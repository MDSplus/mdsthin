#
# Copyright (c) 2024, Massachusetts Institute of Technology All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os
import sys
import time
import ctypes
import socket
import getpass
import logging

from .message import *
from .exceptions import *
from .functions import *

INVALID_MESSAGE_ID = 0

MDSIP_VERSION = 3

SSH_BACKEND_SUBPROCESS = 'subprocess'
SSH_BACKEND_PARAMIKO   = 'paramiko'

class Connection:
    """Implements an MDSip connection to an MDSplus server."""

    def __init__(self,
        url: str,
        timeout: float = 60.0,
        verbose: bool = False,
        ssh_backend: str = SSH_BACKEND_SUBPROCESS,
        ssh_port: int = None,
        sshp_host: str = 'localhost',
        ssh_subprocess_args: list = None,
        ssh_paramiko_options: dict = None,
        ssh_use_plink: bool = False,
    ):
        """
        Initialize an MDSplus connection to a given URL.

        The URL will be parsed as `proto://username@host:port`. The default `proto` is tcp,
        the default `username` is `os.getlogin()`, and the default `port` is 8000.

        For SSH connections you can also specify `ssh_port` as a kwarg, the default is up to the
        backend, but should always be 22. Except for `ssh://`, where `ssh_port` will default to
        `port` if it is specified, otherwise it will be up to the backend. For `sshp://` you can
        also specify `sshp_host` to specify the MDSip host to netcat to after connecting to ssh,
        otherwise it will default to `localhost`.

        Supported protocols:
         * tcp:// - Connect directly to the MDSip server at `host:port` over IPv4.
         * tcp6:// - Connect directly to the MDSip server at `host:port` over IPv6.
         * ssh:// - Connect over SSH to `host:ssh_port` and then spawn `mdsip-server-ssh`.
         * sshp:// - Connect over SSH to `host:ssh_port` and then spawn `nc $sshp_host $port`.

        :param str url: The URL to connect to.
        :param float timeout: The timeout for all socket operations in seconds, defaults to 60s
        :param bool verbose: Enable debug logging for this connection.
        :param str ssh_backend: The backend implementation of ssh to use. Can be either
            'subprocess' or 'paramiko', defaults to 'subprocess'.
        :param int ssh_port: The port to ssh to when using one of the SSH protocols.
        :param str sshp_host: The host to netcat to when using `sshp://`, defaults to 'localhost'.
        :param list ssh_subprocess_args: Additional arguments to pass to the ssh subprocess
            command line when using `SSH_BACKEND_SUBPROCESS` and one of the SSH protocols.
        :param dict ssh_paramiko_options: Additional kwargs to pass to the paramiko connect()
            function when using `SSH_BACKEND_PARAMIKO` and one of the SSH protocols.
        :param bool ssh_use_plink: Attempt to use `plink.exe -batch` instead of `ssh.exe`
            for ssh:// and sshp:// connections. Remember to use `ssh_subprocess_args` to pass any
            necessary arguments.
        :raises TimeoutError: if the connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko socket wrapper fails.
        :raises paramiko.ssh_exception.*: if the paramiko client fails.
        :raises socket.gaierror: if `host` could not be resolved to an IP.
        :raises MdsException: if an unsupported protocol is specified, or if the login fails.
        """

        logging.basicConfig()

        self._logger = logging.getLogger(__name__)
        if verbose:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.WARNING)

        self._socket = None
        self._timeout = timeout
        self._message_id = INVALID_MESSAGE_ID
        self._server_version = None
        self._compression_level = None

        self._ssh_backend = ssh_backend
        self._ssh_port = ssh_port
        self._sshp_host = sshp_host
        self._ssh_subprocess_args = ssh_subprocess_args
        self._ssh_paramiko_options = ssh_paramiko_options
        self._ssh_use_plink = ssh_use_plink

        self._url = url
        self._host = url

        if '://' in self._host:
            self._protocol, self._host = self._host.split('://', maxsplit=1)
        else:
            self._protocol = 'tcp'

        SUPPORTED_PROTOCOLS = ['tcp', 'tcp6', 'ssh', 'sshp']
        if self._protocol not in SUPPORTED_PROTOCOLS:
            raise MdsException(f'Only the following protocols are supported: {", ".join(SUPPORTED_PROTOCOLS)}')

        if '@' in self._host:
            # We use rsplit to allow usernames connection strings like:
            # 'user@example.com@server:port'
            self._username, self._host = self._host.rsplit('@', maxsplit=1)
        else:
            # The username used for the MDSip login packet, and SSH if the protocol is `ssh://` or `sshp://`
            self._username = getpass.getuser()

        if ':' in self._host:
            self._host, self._port = self._host.split(':', maxsplit=1)
            self._port = int(self._port)

            if self._protocol == 'ssh' and self._ssh_port is None:
                self._ssh_port = self._port
        else:
            # The MDSip default port
            self._port = 8000
        self.connect()

    def __del__(self):
        self.disconnect()

    # Used for with statement
    def __enter__(self):
        return self

    # Used for with statement
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.disconnect()

    def connect(self):
        """
        Initialize the socket and do the login handshake.

        :raises TimeoutError: if the connection fails.
        :raises socket.gaierror: if the hostname could not be resolved.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko socket wrapper fails.
        :raises paramiko.ssh_exception.*: if the paramiko client fails.
        :raises MdsException: if the login fails.
        """

        if self._protocol in ['tcp', 'tcp6']:

            if self._protocol == 'tcp':
                socket_family = socket.AF_INET
                socket_type = socket.SOCK_STREAM
            else:
                socket_family = socket.AF_INET6
                socket_type = socket.SOCK_STREAM

            self._socket = socket.socket(socket_family, socket_type)

            self._logger.debug(f'Setting timeout to {self._timeout}s')
            self._socket.settimeout(self._timeout)

            # This causes a massive speed increase
            # It was designed to reduce the number of small packets on the wire, but we use
            # small packets for a lot of things, so it only hurts us
            self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            # Regular MDSplus also sets SO_KEEPALIVE and SO_OOBINLINE

            self._logger.debug(f'Resolving {self._host}')
            address_list = socket.getaddrinfo(self._host, self._port, family=socket_family, type=socket_type)
            self._address = address_list[0][4]

            self._logger.debug(f'Connecting to {self._address}:{self._port}')
            self._socket.connect(self._address)

        elif self._protocol in ['ssh', 'sshp']:

            if self._protocol == 'ssh':
                command = '/bin/sh -l -c mdsip-server-ssh'
            elif self._protocol == 'sshp':
                command = f'nc {self._sshp_host} {self._port}'

            if self._ssh_backend == SSH_BACKEND_SUBPROCESS:

                import shutil
                import subprocess

                if self._ssh_use_plink:
                    ssh = shutil.which('plink')
                    if ssh is None:
                        raise Exception('Unable to find plink.exe')
                else:
                    ssh = shutil.which('ssh')
                    if ssh is None:
                        raise Exception('Unable to find ssh command')

                ssh_command = [ssh]

                if self._ssh_port is not None:
                    if self._ssh_use_plink:
                        ssh_command.append(f'-P{self._ssh_port}')
                    else:
                        ssh_command.append(f'-p{self._ssh_port}')

                if self._ssh_use_plink:
                    ssh_command.append('-batch')

                if self._ssh_subprocess_args is not None:
                    ssh_command.extend(self._ssh_subprocess_args)
                
                ssh_command.append(f'{self._username}@{self._host}')
                ssh_command.append(command)

                ssh_command_print = [ f'"{v}"' if ' ' in v else v for v in ssh_command ]
                self._logger.debug(f'Executing {" ".join(ssh_command_print)}')

                self._ssh_subprocess = subprocess.Popen(
                    ssh_command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    # Do not pipe stderr>stdout or the first packet we recv could be the shell errors from ssh
                    stderr=subprocess.PIPE,
                )

                import threading

                # Why is adding a timeout so hard
                class SubprocessTimeout:
                    def __init__(self, proc, timeout):
                        self._proc = proc
                        self._timer = threading.Timer(interval=timeout, function=self.do_timeout)

                    def __enter__(self):
                        self._timer.start()
                        return self

                    def __exit__(self, exc_type, exc_value, exc_traceback):
                        self._timer.cancel()
                        del self._timer
                    
                    def do_timeout(self):
                        self._proc.terminate()

                class SubprocessSocket:
                    def __init__(self, proc: subprocess.Popen, timeout: float):
                        self._proc = proc
                        self._timeout = timeout

                    def recv(self, size, flags):
                        with SubprocessTimeout(self._proc, self._timeout):
                            return self._proc.stdout.read(size)
                        
                    def recv_into(self, buffer, size, flags):
                        buffer[ : size] = self.recv(size, flags)
                        return size

                    def sendall(self, buffer):
                        with SubprocessTimeout(self._proc, self._timeout):
                            self._proc.stdin.write(buffer)
                            self._proc.stdin.flush()

                    def close(self):
                        self._proc.terminate()
                        self._proc.stdin.close()
                        self._proc.stdout.close()
                        self._proc.stderr.close()
                        self._proc.wait()

                # If stderr is blocking, then we can't check it without locking the whole program up
                try:
                    os.set_blocking(self._ssh_subprocess.stderr.fileno(), False)

                    time.sleep(0.5) # Give the subprocess time to connect

                    for line in self._ssh_subprocess.stderr.readlines():
                        self._logger.warning(line.decode().rstrip())

                except:
                    self._logger.debug('Unable to change SSH subprocess stderr to non-blocking')

                # TODO: Support timeouts

                self._socket = SubprocessSocket(self._ssh_subprocess, self._timeout)

            elif self._ssh_backend == SSH_BACKEND_PARAMIKO:

                import warnings

                # Silence the cryptography deprecation warnings from simply importing paramiko
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    import paramiko

                paramiko_options = {
                    'username': self._username,
                }

                if self._ssh_port is not None:
                    paramiko_options['port'] = int(self._ssh_port)

                if self._ssh_paramiko_options is not None:
                    paramiko_options.update(self._ssh_paramiko_options)

                paramiko_options_print = [ f"{k}={repr(v)}" for k,v in paramiko_options.items() ]
                self._logger.debug(f'Calling paramiko.client.SSHClient.connect("{self._host}", {", ".join(paramiko_options_print)})')

                self._ssh_client = paramiko.client.SSHClient()
                self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._ssh_client.connect(self._host, **paramiko_options)

                class ParamikoSocket:
                    def __init__(self, client, stdin, stdout, stderr):
                        self._client = client
                        self._stdin = stdin
                        self._stdout = stdout
                        self._stderr = stderr

                    def recv(self, size, flags):
                        return self._stdout.read(size)
                        
                    def recv_into(self, buffer, size, flags):
                        buffer[ : size] = self.recv(size, flags)
                        return size

                    def sendall(self, buffer):
                        self._stdin.write(buffer)
                        self._stdin.flush()

                    def close(self):
                        self._stdin.close()
                        self._stdout.close()
                        self._stderr.close()
                        self._client.close()

                self._logger.debug(f'Calling paramiko.client.SSHClient.exec_command("{command}")')
                stdin, stdout, stderr = self._ssh_client.exec_command(command)

                # If stderr is blocking, then we can't check it without locking the whole program up
                try:
                    stderr.channel.settimeout(0.5) # Give the subprocess time to connect

                    for line in stderr.readlines():
                        self._logger.warning(line.rstrip())

                except:
                    self._logger.debug('Unable to change SSH subprocess stderr to non-blocking')

                stdin.channel.settimeout(self._timeout)
                stdout.channel.settimeout(self._timeout)

                self._socket = ParamikoSocket(self._ssh_client, stdin, stdout, stderr)

        msg_login = Message(String(self._username))
        msg_login.ndims = 1
        msg_login.dims[0] = MDSIP_VERSION

        self._logger.debug(f'Sending login request with username="{self._username}"')
        self._send(msg_login)

        # The login response packet is a copy of the login request packet with a few fields changed,
        # so if we process it with self._recv it will wait for data that will never come
        msg_login_buffer = bytearray(ctypes.sizeof(msg_login))
        msg_login_view = memoryview(msg_login_buffer)
        while len(msg_login_view) > 0:
            bytes_read = self._socket.recv_into(msg_login_view, len(msg_login_view), 0)
            msg_login_view = msg_login_view[bytes_read : ]
        
        msg_login = Message.from_buffer_copy(msg_login_buffer)

        if STATUS_NOT_OK(msg_login.status):
            raise MdsException('Failed to login')

        self._compression_level = (msg_login.status & 0x1E) >> 1
        self._client_type = msg_login.client_type

        if msg_login.ndims > 0:
            self._server_version = msg_login.dims[0]

        self._logger.debug(f'Received login response with version={self._server_version} client_type={self._client_type} compression_level={self._compression_level}')

    def disconnect(self):
        """Close the socket."""

        if self._socket:
            self._logger.debug('Disconnecting')
            self._socket.close()
            self._socket = None

    def reconnect(self):
        """Call `disconnect()` and then `connect()`."""
        self.disconnect()
        self.connect()

    def _send(self, msg: Message):

        buffer = msg.pack()

        self._logger.debug(f'Sending packet with msglen={msg.msglen} dtype_id={dtype_to_string(msg.dtype_id)} length={msg.length} dimct={msg.ndims} dims={list(msg.dims)}')
        self._socket.sendall(buffer)

    def _recv(self):

        msg = Message()
        data = Descriptor()

        msg_buffer = bytearray(ctypes.sizeof(msg))
        msg_view = memoryview(msg_buffer)
        while len(msg_view) > 0:
            bytes_read = self._socket.recv_into(msg_view, len(msg_view), 0)
            msg_view = msg_view[bytes_read : ]

        msg = Message.from_buffer_copy(msg_buffer)

        self._logger.debug(f'Received message with msglen={msg.msglen} dtype_id={dtype_to_string(msg.dtype_id)} length={msg.length} dimct={msg.ndims} dims={list(msg.dims)}')

        data_length = msg.msglen - ctypes.sizeof(msg)
        if data_length > 0:
            data_buffer = bytearray(data_length)
            data_view = memoryview(data_buffer)
            while len(data_view) > 0:
                bytes_read = self._socket.recv_into(data_view, len(data_view), 0)
                data_view = data_view[bytes_read : ]

                self._logger.debug(f'Received data packet of {bytes_read} bytes, {data_length - len(data_view)}/{data_length}')

            data = msg.unpack_data(data_buffer)

        return msg, data

    def get(self, expr, *args):
        """
        Evaluate an expression on the remote server and return the result. This works like
        `mdsvalue()` in our other APIs.

        :param str expr: The TDI expression to be evaluated, possibly with `$` placeholders
        :param *args: The optional arguments to be inserted for the placeholders in the
            expression. All native python/numpy types will be converted to Descriptors.
        :return: The result of executing the expression.
        :rtype: :class:`Descriptor`
        :raises TimeoutError: if the connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if the result status indicates an error.
        """

        if expr.strip() == '':
            return Descriptor()

        mget = Message(expr, compression_level=self._compression_level)
        mget.nargs = 1 + len(args)

        self._message_id += 1
        mget.message_id = self._message_id

        self._send(mget)

        for i, arg in enumerate(args):
            marg = Message(arg, compression_level=self._compression_level)
            marg.nargs = mget.nargs
            marg.message_id = mget.message_id
            marg.descriptor_idx = i + 1

            self._send(marg)

        manswer, data = self._recv()

        if STATUS_NOT_OK(manswer.status):
            raise getException(manswer.status)

        return data

    def getObject(self, expr, *args):
        """
        Evaluate a `get()` expression, but the expression will be wrapped in 'SerializeOut'
        and `deserialize()` will be called on the result. This allows you to retrieve data
        with CLASS_R or CLASS_APD, that otherwise cannot be retrieved with a regular `get()`.

        :param str expr: The TDI expression to be evaluated, possibly with `$` placeholders
        :param *args: The optional arguments to be inserted for the placeholders in the
            expression. All native python/numpy types will be converted to Descriptors.
        :return: The result of executing the expression.
        :rtype: :class:`Descriptor`
        :raises TimeoutError: if the connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if the result status indicates an error.
        """
        return self.get(f'SerializeOut(`({expr};))', *args).deserialize(conn=self)

    def put(self, path, expr, *args):
        """
        Put an evaluated expression into a node in the last opened MDSplus tree.

        :param str path: The path to the node to write data into.
        :param str expr: The TDI expression to be evaluated, possibly with `$` placeholders
        :param *args: The optional arguments to be inserted for the placeholders in the
            expression. All native python/numpy types will be converted to Descriptors.
        :raises TimeoutError: if the connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if the result status indicates an error.
        """
        args = [path, expr] + list(args)
        args_format = ','.join('$' * len(args))
        status = self.get(f'TreePut({args_format})', *args).data()

        if STATUS_NOT_OK(status):
            raise getException(status)

    def getMany(self):
        """
        Return a :class:`GetMany` object tied to this connection.

        :return: :class:`GetMany(self)`
        :rtype: :class:`GetMany`
        """

        return GetMany(self)

    def putMany(self):
        """
        Return a :class:`PutMany` object tied to this connection.

        :return: :class:`PutMany(self)`
        :rtype: :class:`PutMany`
        """

        if self.getServerVersion() < (7, 145, 7):
            import warnings
            warnings.warn('putMany is likely broken in MDSplus < 7.145.7, use with caution')

        return PutMany(self)

    def openTree(self, tree: str, shot: int):
        """
        Open an MDSplus tree on a remote server.

        :param str tree: The tree name to open.
        :param int shot: The shot number to open.
        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if the tree could not be opened.
        """

        status = self.get('TreeOpen($,$)', tree, shot).data()

        if STATUS_NOT_OK(status):
            raise getException(status)

    def closeTree(self, tree: str, shot: int):
        """
        Close an MDSplus tree on the remote server.

        :param str tree: The tree name to close.
        :param int shot: The shot number to close.
        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if the tree could not be closed.
        """

        status = self.get('TreeClose($,$)', tree, shot).data()

        if STATUS_NOT_OK(status):
            raise getException(status)

    def closeAllTrees(self):
        """
        Close all open MDSplus trees.

        :return: The number of trees closed.
        :rtype: Descriptor
        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if there was a problem executing the `get()`.
        """

        return self.get("_i=0;WHILE(IAND(TreeClose(),1)) _i++;_i")

    def setDefault(self, path: str):
        """
        Change the current default tree location on the remote server

        :param str path: The tree node path to be set as the new default location.
        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if the tree node could not be found, or the location
            could not be changed.
        """

        status = self.get('TreeSetDefault($)', path).data()

        if STATUS_NOT_OK(status):
            raise getException(status)

    def tcl(self, command: str):
        """
        Execute a mdstcl command and return the result.

        :param str command: The mdstcl command to run.
        :return: The command output from mdstcl.
        :rtype: str
        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if there was a problem executing the command.
        """
        result = self.get('Tcl($,_res);_res', command)
        if result is None:
            return ''
        return result.data()
    
    def getServerVersion(self):
        import re

        show_version = self.tcl('show version')
        matches = re.search(r'MDSplus version: ([0-9]+)\.([0-9]+)\.([0-9]+)', show_version, re.MULTILINE)

        return (int(matches[1]), int(matches[2]), int(matches[3]))

    def mdstcl(self):
        """
        Create a faux mdstcl prompt, calling `tcl()` for each command.

        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        """

        while True:
            # Use sys.stdout to avoid cluttering the python history with TCL commands
            sys.stdout.write('TCL> ')
            sys.stdout.flush()
            command = sys.stdin.readline()

            # Ctrl+D
            if len(command) == 0:
                print()
                break

            command = command.strip()

            # Empty command
            if len(command) == 0:
                continue

            if command == 'exit':
                break

            try:
                result = self.tcl(command)
            except MdsException as e:
                print(e)

            if result is not None:
                print(result, end='')

    def tdic(self):
        """
        Create a faux tdic prompt, calling `get()` for each command.

        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        """

        while True:
            # Use sys.stdout to avoid cluttering the python history with TCL commands
            sys.stdout.write('TDI> ')
            sys.stdout.flush()
            command = sys.stdin.readline()

            # Ctrl+D
            if len(command) == 0:
                print()
                break

            command = command.strip()

            if command == 'exit':
                break

            result = None
            try:
                result = self.get(command)
            except MdsException as e:
                print(e)

            if result is None:
                print(repr(dMISSING()))
            else:
                print(repr(result))

class GetMany:
    """
    Allows you to build a list of expressions to evaluate, reducing the number of network
    transactions needed.

    This must be constructed with a reference to a :class:`Connection`, this be done with
    `connection.getMany()`. You can then call `append()` to add expressions to the list.
    Once the list is complete, you must use `execute()` to send the expressions to the
    server and retrieve the result. This will return a dictionary of the result, or you
    can use `get()` to access the expressions by name.

    Example:
    ```
    gm = c.getMany()
    gm.append('y', '\\IP')
    gm.append('x', 'dim_of(\\IP)')
    result = gm.execute()

    y = gm.get('y')
    x = gm.get('x')
    # or
    y = result['y']
    x = result['x']
    ```
    """

    def __init__(self, connection: Connection):
        self._connection = connection
        self._queries = List()
        self._result = None

    def append(self, name, exp, *args):
        """
        Add a named expression to the list to be evaluated by `execute()`.

        :param str name: The name of the expression to evaluate. This will be how you
            retrieve the data from either the result dictionary or using `get()`.
        :param str expr: The TDI expression to be evaluated, possibly with `$` placeholders.
        :param *args: The optional arguments to be inserted for the placeholders in the
            expression. All native python/numpy types will be converted to Descriptors.
        """
        self._queries.append(Dictionary({
            'name': name,
            'exp': exp,
            'args': list(args),
        }))

    def remove(self, name):
        """
        Remove a named expression from the list

        :param str name: The name of the expression to remove
        """
        for query in self._queries:
            if query['name'] == name:
                self._queries.remove(query)
                break

    def execute(self):
        """
        Execute all expressions in the list by calling `GetManyExecute()` on the remote
        server, and passing the serialized list as data.

        :return: The Dictionary of results from the expressions. In the format of,
            `{ NAME: { 'value': DATA } }` if the expression succeeded, or
            `{ NAME: { 'error': ERROR_STRING } }` if there was an error.
        :rtype: :class:`Dictionary`
        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if the result of GetManyExecute() is an error string, or
            if `get()` encounters an error.
        """
        result = self._connection.get('GetManyExecute($)', self._queries.serialize())

        if isinstance(self._result, String):
            raise MdsException(f'GetMany Error: {self._result.data()}')

        self._result = result.deserialize()
        return self._result

    def get(self, name):
        """
        Get the result of a named expression, or raise an error if the evaluation failed.

        :param str name: The name of the expression
        :return: The resulting data from the expression
        :rtype: :class:`Descriptor`
        :raises MdsException: if `execute()` has not been called, or if the evaluation of
            the expression on the server failed.
        """
        if self._result is None:
            raise MdsException('GetMany has not been executed, call execute() first.')

        if name not in self._result:
            return None

        result = self._result[name]
        if 'value' in result:
            return result['value']

        raise getExceptionFromError(result['error'].data())

class PutMany:
    """
    Allows you to build a list of nodes with expressions to evaluate and store in them,
    reducing the number of network transactions needed.

    This must be constructed with a reference to a :class:`Connection`, this be done with
    `connection.putMany()`. You can then call `append()` to add nodes/expressions to the list.
    Once the list is complete, you must use `execute()` to send the expressions to the
    server and insert the data into each node. This will return a dictionary of the status of
    each node's operation, or you can use `checkStatus()` to check a given node.

    If you wish to store the result of an expression in a node, you must prefix the expression with '`'.

    Example:
    ```
    pm = c.putMany()
    pm.append('NODE_A', '$', 42)
    pm.append('NODE_B', '$', numpy.array([1, 2, 3, 4]))
    pm.append('NODE_C', 'SerializeIn($)', Signal(data, None, dim).serialize())
    result = pm.execute()

    gm.checkStatus('a')
    # or
    if result['a'] != 'Success':
        pass
    ```
    """


    def __init__(self, connection: Connection):
        self._connection = connection
        self._queries = List()
        self._result = Dictionary()

    def append(self, node, exp, *args):
        """
        Add a node/expression to the list to be evaluated and inserted by `execute()`

        :param str node: The node to insert the evaluated expression into.
        :param str expr: The TDI expression to be evaluated, possibly with `$` placeholders
        :param *args: The optional arguments to be inserted for the placeholders in the
            expression. All native python/numpy types will be converted to Descriptors
        """
        self._queries.append(Dictionary({
            'node': node,
            'exp': exp,
            'args': list(args),
        }))

    def remove(self, node):
        """
        Remove a node/expression from the list

        :param str name: The node to remove from the list
        """
        for query in self._queries:
            if query['node'] == node:
                self._queries.remove(query)
                break

    def execute(self):
        """
        Execute and insert all expressions in the list by calling `PutManyExecute()`
        on the remote server, and passing the serialized list as data.

        :return: The Dictionary of results from the expressions. In the format of,
            `{ NAME: 'Success' }` if the expression succeeded, or
            `{ NAME: ERROR_STRING } }` if there was an error.
        :rtype: :class:`Dictionary`
        :raises TimeoutError: if the network connection fails.
        :raises BrokenPipeError: if the SSH subprocess fails.
        :raises OSError: if the paramiko client fails.
        :raises MdsException: if the result of PutManyExecute() is an error string, or
            if `get()` encounters an error.
        """
        result = self._connection.get('PutManyExecute($)', self._queries.serialize())

        if isinstance(self._result, String):
            raise MDSplusException(f'PutMany Error: {self._result.data()}')

        self._result = result.deserialize(conn=self)
        return self._result

    def checkStatus(self, node):
        """
        Check the status of inserting the data into a given node.

        :param str name: The node to check
        :return: The resulting "Success" string for the node
        :rtype: :class:`Descriptor`
        :raises MdsException: if `execute()` has not been called, or if the evaluation or
            insertion of the expression on the server failed.
        """
        if self._result is None:
            raise MdsException('PutMany has not been executed, call execute() first.')

        if node not in self._result:
            return None

        result = self._result[node]
        if self.result[node] != "Success":
            raise getExceptionFromError(self._result[node])

        return self.result[node]
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
import ctypes
import socket

from .message import *
from .exceptions import *
from .functions import *

INVALID_MESSAGE_ID = 0

MDSIP_VERSION = 3

class Connection:
    """Implements an MDSip connection to an MDSplus server."""
    
    def __init__(self, url: str, username: str = os.getlogin(), timeout: float = 60.0):
        """
        Initialize an MDSplus connection to a given URL.

        The URL will be parsed as `PROTO://HOSTNAME:PORT`. The default PROTO is tcp,
        and the default PORT is 8000.

        :param str url: The URL to connect to.
        :param str username: The username to connect with, defaults to `os.getlogin()`.
        :param float timeout: The timeout for all socket operations in seconds, defaults to 10s
        :raises TimeoutError: if the connection fails.
        :raises socket.gaierror: if the hostname could not be resolved.
        :raises MdsException: if an unsupported protocol is specified, or if the login fails.
        """

        self._socket = None
        self._timeout = timeout
        self._message_id = INVALID_MESSAGE_ID
        self._server_version = None
        self._compression_level = None

        self._username = username
        self._host = url
        self._protocol = 'tcp'
        if '://' in self._host:
            self._protocol, self._host = self._host.split('://', maxsplit=1)
        
        self._port = 8000
        if ':' in self._host:
            self._host, self._port = self._host.split(':', maxsplit=1)
            self._port = int(self._port)

        if self._protocol not in ['tcp', 'tcp6']:
            raise MdsException('Only tcp:// and tcp6:// are supported')
        
        self.connect()

    def __del__(self):
        self.disconnect()

    # Used for with statement
    def __enter__(self):
        self.connect()

    # Used for with statement
    def __exit__(self):
        self.disconnect()
        
    def connect(self):
        """
        Initialize the socket and do the login handshake.

        :raises TimeoutError: if the connection fails.
        :raises socket.gaierror: if the hostname could not be resolved.
        :raises MdsException: if the login fails.
        """
        
        if self._protocol == 'tcp':
            socket_family = socket.AF_INET
            socket_type = socket.SOCK_STREAM
        
        elif self._protocol == 'tcp6':
            socket_family = socket.AF_INET6
            socket_type = socket.SOCK_STREAM

        self._socket = socket.socket(socket_family, socket_type)

        self._socket.settimeout(self._timeout)
        
        # This causes a massive speed increase
        # It was designed to reduce the number of small packets on the wire, but we use
        # small packets for a lot of things, so it only hurts us
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        # Regular MDSplus also sets SO_KEEPALIVE and SO_OOBINLINE

        address_list = socket.getaddrinfo(self._host, self._port, family=socket_family, type=socket_type)
        self._address = address_list[0][4]

        self._socket.connect(self._address)

        mlogin = Message(String(self._username))
        mlogin.ndims = 1
        mlogin.dims[0] = MDSIP_VERSION

        self._send(mlogin)

        # The login response does not contain data
        self._socket.recv_into(mlogin, ctypes.sizeof(mlogin), socket.MSG_WAITALL)

        if STATUS_NOT_OK(mlogin.status):
            raise MdsException('Failed to login')
        
        self._compression_level = (mlogin.status & 0x1E) >> 1
        self._client_type = mlogin.client_type
        
        if mlogin.ndims > 0:
            self.version = mlogin.dims[0]

    def disconnect(self):
        """Close the socket."""

        if self._socket:
            self._socket.close()
            self._socket = None

    def reconnect(self):
        """Call `disconnect()` and then `connect()`."""
        self.disconnect()
        self.connect()

    def _send(self, msg: Message):

        buffer = msg.pack()
        self._socket.sendall(buffer)

    def _recv(self):

        msg = Message()
        data = Descriptor()

        bytes_read = self._socket.recv_into(msg, ctypes.sizeof(msg), socket.MSG_WAITALL)
        if bytes_read < ctypes.sizeof(msg):
            raise TimeoutError

        data_length = msg.msglen - ctypes.sizeof(Message)
        if data_length > 0:
            buffer = bytearray(data_length)

            view = memoryview(buffer)
            while len(view) > 0:
                bytes_read = self._socket.recv_into(view, len(view), socket.MSG_WAITALL)
                if not bytes_read:
                    break
                
                view = view[bytes_read : ]

            if len(view) > 0:
                raise TimeoutError
            
            data = msg.unpack_data(buffer)

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
        :raises MdsException: if the result status indicates an error.
        """
        args = [path, expr] + list(args)
        args_format = ','.join('$' * len(args))
        status = self.get(f'TreePut({args_format})', *args)

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
        
        return PutMany(self)

    def openTree(self, tree: str, shot: int):
        """
        Open an MDSplus tree on a remote server.

        :param str tree: The tree name to open.
        :param int shot: The shot number to open.
        :raises TimeoutError: if the network connection fails.
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
        :raises MdsException: if there was a problem executing the `get()`.
        """

        return self.get("_i=0;WHILE(IAND(TreeClose(),1)) _i++;_i")

    def setDefault(self, path: str):
        """
        Change the current default tree location on the remote server

        :param str path: The tree node path to be set as the new default location.
        :raises TimeoutError: if the network connection fails.
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
        :raises MdsException: if there was a problem executing the command.
        """
        result = self.get('Tcl($,_res);_res', command)
        if result is None:
            return ''
        return result.data()
    
    def mdstcl(self):
        """
        Create a faux mdstcl prompt, calling `tcl()` for each command.

        :raises TimeoutError: if the network connection fails.
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
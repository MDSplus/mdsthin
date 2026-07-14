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

import ctypes
import socket
import threading
import unittest

from ..connection import Connection, MDSIP_VERSION
from ..message import Message

class PeerCloseTest(unittest.TestCase):
    """
    Regression tests for the peer-closed-connection busy-loop (issue #8).

    A fake mdsip server accepts the connection and then closes the socket at
    various points. The client must raise BrokenPipeError instead of spinning
    forever in its recv_into() loops (recv_into() returns 0 at EOF, which used
    to go unchecked).

    No real server is needed, so these tests always run.
    """

    def _start_server(self, handler):
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 0))
        server.listen(1)
        port = server.getsockname()[1]

        def run():
            conn, _ = server.accept()
            try:
                handler(conn)
            finally:
                conn.close()
                server.close()

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.addCleanup(server.close)
        return port

    @staticmethod
    def _read_message(conn):
        header = b''
        while len(header) < ctypes.sizeof(Message):
            chunk = conn.recv(ctypes.sizeof(Message) - len(header))
            if not chunk:
                return None
            header += chunk

        msg = Message.from_buffer_copy(header)
        remaining = msg.msglen - ctypes.sizeof(Message)
        while remaining > 0:
            chunk = conn.recv(min(remaining, 4096))
            if not chunk:
                return None
            remaining -= len(chunk)

        return msg

    @classmethod
    def _send_login_response(cls, conn, msg):
        msg.status = 1
        msg.ndims = 1
        msg.dims[0] = MDSIP_VERSION
        conn.sendall(bytes(msg))

    def test_close_during_login(self):

        def handler(conn):
            self._read_message(conn)
            # close without sending the login response

        port = self._start_server(handler)

        with self.assertRaises(BrokenPipeError):
            Connection(f'127.0.0.1:{port}', timeout=5)

    def test_close_before_reply(self):

        def handler(conn):
            msg = self._read_message(conn)
            self._send_login_response(conn, msg)

            # read the GET request, then close without replying
            self._read_message(conn)

        port = self._start_server(handler)

        conn = Connection(f'127.0.0.1:{port}', timeout=5)

        with self.assertRaises(BrokenPipeError):
            conn.get('1')

    def test_close_mid_reply(self):

        def handler(conn):
            msg = self._read_message(conn)
            self._send_login_response(conn, msg)

            self._read_message(conn)

            # send only part of the response message header, then close
            conn.sendall(bytes(msg)[: ctypes.sizeof(Message) // 2])

        port = self._start_server(handler)

        conn = Connection(f'127.0.0.1:{port}', timeout=5)

        with self.assertRaises(BrokenPipeError):
            conn.get('1')

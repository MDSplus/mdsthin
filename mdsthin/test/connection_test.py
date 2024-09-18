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

import getpass
import unittest

from ..connection import *
from ..functions import *

class ConnectionTest(unittest.TestCase):

    SERVER = ''
    PORT = None
    USERNAME = None
    TIMEOUT = 5
    SSH_ENABLED = False

    @classmethod
    def setUpClass(cls):
        if cls.SERVER != '':
            url = cls.SERVER

            if cls.USERNAME is not None:
                url = f'{cls.USERNAME}@{url}'
            else:
                cls.USERNAME = getpass.getuser()

            if cls.PORT is not None:
                url = f'{url}:{cls.PORT}'
            else:
                cls.PORT = 8000

            cls.conn = Connection(url)

    def setUp(self):
        if self.SERVER == '':
            raise unittest.SkipTest("--server was not specified")

    def test_tdi_types(self):

        tests = [
            { 'type': Int32,   'exp': '42',        'value': 42, },
            { 'type': UInt8,   'exp': '42BU',      'value': 42, },
            { 'type': UInt16,  'exp': '42WU',      'value': 42, },
            { 'type': UInt32,  'exp': '42LU',      'value': 42, },
            { 'type': UInt64,  'exp': '42QU',      'value': 42, },
            { 'type': Int8,    'exp': '42B',       'value': 42, },
            { 'type': Int16,   'exp': '42W',       'value': 42, },
            { 'type': Int32,   'exp': '42L',       'value': 42, },
            { 'type': Int64,   'exp': '42Q',       'value': 42, },
            { 'type': Float32, 'exp': '3.14159',   'value': 3.14159, },
            { 'type': Float32, 'exp': '3.14159F0', 'value': 3.14159, },
            { 'type': Float64, 'exp': '3.14159D0', 'value': 3.14159, },
            { 'type': Float64, 'exp': '3.14159G0', 'value': 3.14159, },
            # { 'type': Float128, 'exp': '3.14159H0', },

            { 'type': Float32, 'exp': 'F_FLOAT(3.14159)', 'value': 3.14159, },
            # { 'type': Float64, 'exp': 'D_FLOAT(3.14159)', 'value': 3.14159, },
            { 'type': Float64, 'exp': 'G_FLOAT(3.14159)', 'value': 3.14159, },

            { 'type': Int32Array, 'exp': '[ [2, 4], [6, 8] ]',     'value': numpy.array([ [2, 4], [6, 8] ], dtype=numpy.int32) },
            { 'type': Int8Array,  'exp': '[ [2B, 4B], [6B, 8B] ]', 'value': numpy.array([ [2, 4], [6, 8] ], dtype=numpy.int8) },
            { 'type': Int16Array, 'exp': '[ [2W, 4W], [6W, 8W] ]', 'value': numpy.array([ [2, 4], [6, 8] ], dtype=numpy.int16) },
            { 'type': Int32Array, 'exp': '[ [2L, 4L], [6L, 8L] ]', 'value': numpy.array([ [2, 4], [6, 8] ], dtype=numpy.int32) },
            { 'type': Int64Array, 'exp': '[ [2Q, 4Q], [6Q, 8Q] ]', 'value': numpy.array([ [2, 4], [6, 8] ], dtype=numpy.int64) },
        ]

        for info in tests:
            name = f"get('{info['exp']}')"
            with self.subTest(name):

                data = self.conn.get(info['exp'])
                self.assertEqual(type(data), info['type'])

                if type(info['value']) is float:
                    self.assertAlmostEqual(data.data(), info['value'], places=5)
                else:
                    self.assertEqual(data, info['value'])

        for info in tests:
            name = f"getObject('{info['exp']}')"
            with self.subTest(name):

                data = self.conn.getObject(info['exp'])
                self.assertEqual(type(data), info['type'])

                if type(info['value']) is float:
                    self.assertAlmostEqual(data.data(), info['value'], places=5)
                else:
                    self.assertEqual(data, info['value'])

    def test_getmany(self):

        expected_result = Descriptor({
            String('a'): Descriptor({ String('value'): Int32(42) }),
            String('b'): Descriptor({ String('value'): String('Hello, World!') }),
            String('c'): Descriptor({ String('error'): String('%TREE-W-NOT_OPEN, Tree not currently open') }),
        })

        gm = self.conn.getMany()
        gm.append('a', '42')
        gm.append('b', '"Hello, World!"')
        gm.append('c', 'asdf')
        result = gm.execute()

        self.assertEqual(result, expected_result)
        self.assertEqual(gm.get('a'), 42)
        self.assertEqual(gm.get('b'), 'Hello, World!')
        self.assertRaises(TreeNOT_OPEN, gm.get, 'c')

    def test_root_whoami(self):

        root_conn = Connection(f'root@{self.SERVER}')

        whoami = root_conn.get('whoami()').data()
        self.assertEqual(whoami, 'nobody', msg='Claiming to be root should map you to nobody.')

    # We're a little limited in what we can test here
    def test_ssh_subprocess(self):
        if not self.SSH_ENABLED:
            raise unittest.SkipTest('--ssh was not specified')

        # We can only test a connection string without a username if the username is default
        if self.USERNAME == getpass.getuser():
            url = f'ssh://{self.SERVER}'
            with Connection(url, timeout=self.TIMEOUT) as test_conn:
                whoami = test_conn.get('whoami()').data()
                self.assertEqual(
                    whoami, self.USERNAME,
                    f'Connection("{url}") failed'
                )

        url = f'ssh://{self.USERNAME}@{self.SERVER}'
        with Connection(url, timeout=self.TIMEOUT, ssh_port=22) as test_conn:
            whoami = test_conn.get('whoami()').data()
            self.assertEqual(
                whoami, self.USERNAME,
                f'Connection("{url}", ssh_port=22) failed'
            )

        url = f'ssh://{self.USERNAME}@{self.SERVER}:22'
        with Connection(url, timeout=self.TIMEOUT) as test_conn:
            whoami = test_conn.get('whoami()').data()
            self.assertEqual(
                whoami, self.USERNAME,
                f'Connection("{url}") failed'
            )

        # TODO: Test ssh_subprocess_args
        # TODO: Test plink

    def test_ssh_paramiko(self):
        if not self.SSH_ENABLED:
            raise unittest.SkipTest('--ssh was not specified')
        
        try:
            import warnings

            # Silence the cryptography deprecation warnings from simply importing paramiko
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                import paramiko

            # We can only test a connection string without a username if the username is default
            if self.USERNAME == getpass.getuser():
                url = f'ssh://{self.SERVER}'
                with Connection(url, timeout=self.TIMEOUT, ssh_backend='paramiko') as test_conn:
                    whoami = test_conn.get('whoami()').data()
                    self.assertEqual(
                        whoami, self.USERNAME,
                        f'Connection("{url}", ssh_backend="paramiko") failed'
                    )

            url = f'ssh://{self.USERNAME}@{self.SERVER}'
            with Connection(url, timeout=self.TIMEOUT, ssh_port=22, ssh_backend='paramiko') as test_conn:
                whoami = test_conn.get('whoami()').data()
                self.assertEqual(
                    whoami, self.USERNAME,
                    f'Connection("{url}", ssh_port=22, ssh_backend="paramiko") failed'
                )

            url = f'ssh://{self.USERNAME}@{self.SERVER}:22'
            with Connection(url, timeout=self.TIMEOUT, ssh_backend='paramiko') as test_conn:
                whoami = test_conn.get('whoami()').data()
                self.assertEqual(
                    whoami, self.USERNAME,
                    f'Connection("{url}", ssh_backend="paramiko") failed'
                )

            # TODO: Test ssh_paramiko_options

        except ImportError:
            self.skipTest('Cannot import paramiko')

    def test_sshp_subprocess(self):
        if not self.SSH_ENABLED:
            raise unittest.SkipTest('--ssh was not specified')

        # We can only test a connection string without a username if the username is default
        if self.USERNAME == getpass.getuser():
            url = f'sshp://{self.SERVER}'
            with Connection(url, timeout=self.TIMEOUT) as test_conn:
                whoami = test_conn.get('whoami()').data()
                self.assertEqual(
                    whoami, self.USERNAME,
                    f'Connection("{url}") failed'
                )

        # We can only test a connection string without a port if the port is 8000
        if self.PORT == 8000:
            url = f'sshp://{self.USERNAME}@{self.SERVER}'
            with Connection(url, timeout=self.TIMEOUT, ssh_port=22) as test_conn:
                whoami = test_conn.get('whoami()').data()
                self.assertEqual(
                    whoami, self.USERNAME,
                    f'Connection("{url}", ssh_port=22) failed'
                )

        url = f'sshp://{self.USERNAME}@{self.SERVER}:{self.PORT}'
        with Connection(url, timeout=self.TIMEOUT) as test_conn:
            whoami = test_conn.get('whoami()').data()
            self.assertEqual(
                whoami, self.USERNAME,
                f'Connection("{url}") failed'
            )

        url = f'sshp://{self.USERNAME}@{self.SERVER}:{self.PORT}'
        with Connection(url, timeout=self.TIMEOUT, ssh_port=22) as test_conn:
            whoami = test_conn.get('whoami()').data()
            self.assertEqual(
                whoami, self.USERNAME,
                f'Connection("{url}", ssh_port=22) failed'
            )
            
        # TODO: Test plink

    def test_sshp_paramiko(self):
        if not self.SSH_ENABLED:
            raise unittest.SkipTest('--ssh was not specified')
        
        try:
            import warnings

            # Silence the cryptography deprecation warnings from simply importing paramiko
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                import paramiko

            # We can only test a connection string without a username if the username is default
            if self.USERNAME == getpass.getuser():
                url = f'sshp://{self.SERVER}'
                with Connection(url, timeout=self.TIMEOUT, ssh_backend='paramiko') as test_conn:
                    whoami = test_conn.get('whoami()').data()
                    self.assertEqual(
                        whoami, self.USERNAME,
                        f'Connection("{url}", ssh_backend="paramiko") failed'
                    )

            # We can only test a connection string without a port if the port is 8000
            if self.PORT == 8000:
                url = f'sshp://{self.USERNAME}@{self.SERVER}'
                with Connection(url, timeout=self.TIMEOUT, ssh_port=22, ssh_backend='paramiko') as test_conn:
                    whoami = test_conn.get('whoami()').data()
                    self.assertEqual(
                        whoami, self.USERNAME,
                        f'Connection("{url}", ssh_port=22, ssh_backend="paramiko") failed'
                    )

            url = f'sshp://{self.USERNAME}@{self.SERVER}:{self.PORT}'
            with Connection(url, timeout=self.TIMEOUT, ssh_backend='paramiko') as test_conn:
                whoami = test_conn.get('whoami()').data()
                self.assertEqual(
                    whoami, self.USERNAME,
                    f'Connection("{url}", ssh_backend="paramiko") failed'
                )

            url = f'sshp://{self.USERNAME}@{self.SERVER}:{self.PORT}'
            with Connection(url, timeout=self.TIMEOUT, ssh_port=22, ssh_backend='paramiko') as test_conn:
                whoami = test_conn.get('whoami()').data()
                self.assertEqual(
                    whoami, self.USERNAME,
                    f'Connection("{url}", ssh_port=22, ssh_backend="paramiko") failed'
                )

        except ImportError:
            self.skipTest('Cannot import paramiko')

    def test_empty_get(self):

        result = self.conn.get('')
        self.assertEqual(type(result), Descriptor)
        self.assertEqual(result.data(), None)


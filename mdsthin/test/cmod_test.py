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

import numpy
import getpass
import unittest

from ..connection import *
from ..functions import *

class CModTest(unittest.TestCase):

    SERVER = ''

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
            cls.conn.openTree('cmod', 1090909009)

    def setUp(self):
        if self.SERVER == '':
            raise unittest.SkipTest("--server and --cmod were not specified")

    def test_open_close_tree(self):

        self.conn.openTree('cmod', -1)
        self.conn.closeTree('cmod', -1)

    def test_tstart(self):

        self.assertEqual(self.conn.get('TSTART'), -4.0)

        # TSTART is DTYPE_F, this tests convert_float
        self.assertEqual(self.conn.getObject('TSTART'), -4.0)

    def test_ip(self):

        first10 = numpy.array([ 0, 0, -2.0493028, 313.1422, 2.0493028, 0, 311.0929, -2.0493028, 309.0436, 311.0929 ], dtype=numpy.float32)

        data = self.conn.get('\\IP').data()

        self.assertTrue((data[ : 10] == first10).all())

    def test_checkcamac(self):

        self.assertRaises(TdiINVCLADTY, self.conn.get, 'ADMIN.CHECKCAMAC')

        compare = Action(Dispatch(2, 'ALCDATA_ANALYSIS', 'INIT', 999, ''), EXT_FUNCTION(None, 'CheckCamacServers'), '', None, None)

        data = self.conn.getObject('ADMIN.CHECKCAMAC')

        self.assertEqual(data, compare)
    
    def test_getnci(self):

        tstart_fullpath = self.conn.get('getnci(TSTART, "FULLPATH")').data()

        self.assertEqual(tstart_fullpath, '\\CMOD::TOP:TSTART')

        all_actions = self.conn.get('getnci("***", "FULLPATH", "ACTION")').data()

        self.assertEqual(len(all_actions), 1421)

        all_actions_size = self.conn.get('size(getnci("***", "FULLPATH", "ACTION"))').data()

        self.assertEqual(len(all_actions), all_actions_size)

        all_actions_status = self.conn.get('getnci("***", "STATUS", "ACTION")').data()

        first10 = [1, 1, 1, 1, 1, 0, 0, 0, 0, 1]
        self.assertListEqual(all_actions_status[ : 10 ].tolist(), first10)

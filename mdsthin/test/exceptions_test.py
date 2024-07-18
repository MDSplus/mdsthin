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

import unittest

from ..exceptions import *

class ExceptionsTest(unittest.TestCase):

    def test_status(self):

        self.assertTrue(STATUS_OK(TreeSUCCESS.status))
        self.assertFalse(STATUS_NOT_OK(TreeSUCCESS.status))
        
        self.assertTrue(STATUS_NOT_OK(DevCAMERA_NOT_FOUND.status))
        self.assertFalse(STATUS_OK(DevCAMERA_NOT_FOUND.status))

        self.assertEqual(STATUS_FACILITY(TreeNODATA.status), 4049)
        self.assertEqual(STATUS_MESSAGE(TreeNODATA.status), 4124)
        self.assertEqual(STATUS_SEVERITY(TreeNODATA.status), 2)

    def test_get_exception(self):

        self.assertEqual(getException(65545), MDSplusSUCCESS)

        self.assertEqual(getException(265388200), TreeNOT_OPEN)

        unknown_exception = getException(1234) 
        self.assertEqual(type(unknown_exception), MdsException)
        self.assertEqual(str(unknown_exception), 'Unknown status: 1234')

    def test_get_exception_from_error(self):
        
        self.assertEqual(getExceptionFromError("%TREE-W-NOT_OPEN, Tree not currently open"), TreeNOT_OPEN)
        
        self.assertEqual(getExceptionFromError("%TREE-W-NOT_OPEN, This part doesn't matter"), TreeNOT_OPEN)
        
        unknown_exception = getExceptionFromError("This part definitely matters")
        self.assertEqual(type(unknown_exception), MdsException)
        self.assertEqual(str(unknown_exception), 'This part definitely matters')

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
import numpy
import unittest

from ..connection import *
from ..functions import *

class WriteTest(unittest.TestCase):

    ENABLED = False
    PORT = 12345

    @classmethod
    def setUpClass(cls):
        import atexit
        import shutil
        import tempfile
        import subprocess

        if cls.ENABLED:

            # Attempt to find the mdsip executable
            mdsip = shutil.which('mdsip')
            if mdsip is None:
                cls.ENABLED = False
                return

            # Generate a temporary directory for our config and tree files
            cls.tempdir = tempfile.mkdtemp('-mdsthin-write-test')

            # We need a valid mdsip.hosts in order to spawn a mdsip server
            cls.mdsip_hosts_filename = os.path.join(cls.tempdir, 'mdsip.hosts')
            with open(cls.mdsip_hosts_filename, 'wt') as file:
                file.write('* | MAP_TO_LOCAL\n')

            # Inform the process to put tree files in the temporary directory
            mdsip_env = dict(os.environ)
            mdsip_env['thintest_path'] = cls.tempdir

            # Spawn the mdsip server
            cls.mdsip_process = subprocess.Popen(
                [
                    mdsip,
                    '-h', cls.mdsip_hosts_filename,
                    '-p', str(cls.PORT),
                    '-c', '0',
                    '-s'
                ],
                env=mdsip_env,
                # Disable output from the mdsip server, comment out to debug
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Give the process time to start
            time.sleep(0.1)

            # Ensure that we kill the process even if we don't gracefully shutdown
            atexit.register(subprocess.Popen.terminate, cls.mdsip_process)

            # Setup a new connection to the server we spawned
            cls.mdsip_connection_url = f'localhost:{cls.PORT}'
            cls.conn = Connection(cls.mdsip_connection_url)

            # Create our tree and write the tree files to disk
            cls.conn.tcl("edit thintest /new")
            cls.conn.tcl("add node num /usage=numeric")
            cls.conn.tcl("add node str /usage=text")
            cls.conn.tcl("add node sig /usage=signal")
            cls.conn.tcl("write")
            cls.conn.tcl("close")
            cls.conn.tcl("set tree thintest /shot=-1")
            cls.conn.tcl("create pulse 1") # The readonly tree

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):

        if cls.ENABLED:
            # Close the connection
            cls.conn.disconnect()

            # Kill the mdsip server (this could be handled by atexit, but good to stop it before trying to delete the files)
            cls.mdsip_process.terminate()

            # Cleanup the config and tree files
            files = [
                cls.mdsip_hosts_filename,
                os.path.join(cls.tempdir, 'thintest_model.tree'),
                os.path.join(cls.tempdir, 'thintest_model.datafile'),
                os.path.join(cls.tempdir, 'thintest_model.characteristics'),
                os.path.join(cls.tempdir, 'thintest_001.tree'),
                os.path.join(cls.tempdir, 'thintest_001.datafile'),
                os.path.join(cls.tempdir, 'thintest_001.characteristics'),
            ]

            for file in files:
                try:
                    os.remove(file)
                except FileNotFoundError:
                    pass

            # Cleanup the temporary directory
            os.rmdir(cls.tempdir)

        return super().tearDownClass()

    def setUp(self):
        if not self.ENABLED:
            raise unittest.SkipTest('--write was not specified or it was unable to find mdsip executable')
        
        # Open a tree for the tests to use
        self.conn.openTree('thintest', -1)

    def test_numeric(self):

        INTEGER_ARRAY = [ [2, 4], [6, 8], [16, 32] ]
        FLOAT_ARRAY = [ [1.0, 1.5], [2.0, 2.5], [3.0, 3.5] ]

        tests = [
            { 'value': UInt8(42) },
            { 'value': UInt16(42) },
            { 'value': UInt32(42) },
            { 'value': UInt64(42) },
            { 'value': Int8(42) },
            { 'value': Int16(42) },
            { 'value': Int32(42) },
            { 'value': Int64(42) },
            { 'value': Float32(42.0) },
            { 'value': Float64(42.0) },
            { 'value': UInt8Array(INTEGER_ARRAY) },
            { 'value': UInt16Array(INTEGER_ARRAY) },
            { 'value': UInt32Array(INTEGER_ARRAY) },
            { 'value': UInt64Array(INTEGER_ARRAY) },
            { 'value': Int8Array(INTEGER_ARRAY) },
            { 'value': Int16Array(INTEGER_ARRAY) },
            { 'value': Int32Array(INTEGER_ARRAY) },
            { 'value': Int64Array(INTEGER_ARRAY) },
            { 'value': Float32Array(FLOAT_ARRAY) },
            { 'value': Float64Array(FLOAT_ARRAY) },
        ]

        for info in tests:
            self.conn.put('num', '$', info['value'])
            self.assertEqual(self.conn.get('num'), info['value'])

            # Reset the value each loop
            self.conn.put('num', '*')

        self.conn.put('num', '12345Q')
        self.assertEqual(self.conn.get('num'), Int64(12345))

        self.conn.put('num', '[1Q, 2Q, 3Q, 4Q]')
        self.assertEqual(self.conn.get('num'), Int64Array([ 1, 2, 3, 4 ]))
    
    def test_text(self):

        tests = [
            { 'value': String("Hello, World!") },
            { 'value': StringArray([ "one", "seven", "thirteen" ]) },
        ]

        for info in tests:
            self.conn.put('str', '$', info['value'])
            self.assertEqual(self.conn.get('str'), info['value'])

            # Reset the value each loop
            self.conn.put('str', '*')

        self.conn.put('str', '"Hello, World!"')
        self.assertEqual(self.conn.get('str'), String("Hello, World!"))

        self.conn.put('str', '["one", "seven", "thirteen"]')
        self.assertEqual(self.conn.get('str'), StringArray([ "one", "seven", "thirteen" ]))
    
    def test_signal(self):

        data = numpy.array([ 1, 2, 3, 4])
        times = numpy.array([ 0.1, 0.2, 0.3, 0.4 ])
        signal = Signal(data, None, times)

        self.conn.put('sig', '`SerializeIn($)', signal.serialize())
        self.assertEqual(self.conn.getObject('sig'), signal)

        # Reset the value
        self.conn.put('sig', '*')

        self.conn.put('sig', 'BUILD_SIGNAL([1Q, 2Q, 3Q, 4Q], *, [0.1D0, 0.2D0, 0.3D0, 0.4D0])')
        self.assertEqual(self.conn.getObject('sig'), signal)

        # Reset the value
        self.conn.put('sig', '*')

        self.conn.put('sig', '`SerializeIn($)', BUILD_SIGNAL(data, None, times).serialize())
        self.assertEqual(self.conn.getObject('sig'), signal)

    def test_putmany(self):
        if self.conn.getServerVersion() < (7, 145, 7):
            raise unittest.SkipTest('Disabled for MDSplus < 7.145.7')

        try:
            pm = self.conn.putMany()
            pm.append('num', '$', Int32(42))
            pm.append('str', '$', String("Hello, World!"))
            pm.append('sig', '`SerializeIn($)', Signal(1, 2, 3).serialize())
            pm.execute()

            self.assertEqual(self.conn.get('num'), Int32(42))
            self.assertEqual(self.conn.get('str'), String("Hello, World!"))
            self.assertEqual(self.conn.getObject('sig'), Signal(1, 2, 3))

        except LibKEYNOTFOU:
            raise unittest.SkipTest('Disabled when PutManyExecute is missing from libMdsObjectsCppShr')

    def test_permissions(self):
        import platform

        if platform.system() == 'Windows':
            raise unittest.SkipTest('Disabled on Windows')
        
        # Change all the readonly tree files to be readonly
        filenames = [
            os.path.join(self.tempdir, 'thintest_001.tree'),
            os.path.join(self.tempdir, 'thintest_001.datafile'),
            os.path.join(self.tempdir, 'thintest_001.characteristics'),
        ]
        for filename in filenames:
            os.chmod(filename, 0o400)

        # Open the readonly tree
        self.conn.openTree('thintest', 1)

        self.assertRaises(TreeFAILURE, self.conn.put, 'num', '42')

        self.conn.closeTree('thintest', 1)
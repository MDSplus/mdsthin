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

import argparse

from . import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='mdsthin.test')

    parser.add_argument(
        '--server',
        default=None,
        help='Server to connect to'
    )

    parser.add_argument(
        '--port',
        default=None,
        help='Port to connect to'
    )

    parser.add_argument(
        '--username',
        default=None,
        help='Username to connect with'
    )

    parser.add_argument(
        '--ssh',
        default=False,
        action='store_const', const=True,
        help='Run SSH test cases by connecting to the --server over SSH'
    )

    parser.add_argument(
        '--cmod',
        default=False,
        action='store_const', const=True,
        help='Run C-Mod specific test'
    )

    parser.add_argument(
        '--write',
        default=False,
        action='store_const', const=True,
        help='Run Write tests by spinning up a local mdsip server'
    )

    parser.add_argument(
        'unittest',
        nargs='*',
        help='Arguments to unittest.main()'
    )

    args, extra = parser.parse_known_args()

    run_mdsthin_tests(
        server=args.server,
        port=args.port,
        username=args.username,
        ssh_tests=args.ssh,
        cmod_tests=args.cmod,
        write_tests=args.write,
        # unittest arguments
        argv=[ parser.prog, *extra],
    )


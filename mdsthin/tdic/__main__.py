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

from ..connection import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='mdsthin.tdic')

    parser.add_argument(
        'url',
        help='URL to connect to. Allowed protocols are `tcp://`, `tcp6://`, `ssh://` and `sshp://`, defaults to `tcp://`.'
    )

    parser.add_argument(
        '--timeout',
        default=None,
        required=False,
        help='The timeout for all socket operations in seconds, defaults to 60s.'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_const',
        const=True,
        default=False,
        required=False,
        help='Enable debug logging.'
    )

    parser.add_argument(
        '--ssh-backend',
        default=None,
        required=False,
        help='The backend implementation of ssh to use. Can be either "subprocess" or "paramiko", defaults to "subprocess".'
    )

    parser.add_argument(
        '--ssh-port',
        default=None,
        required=False,
        help='The port to ssh to when using one of the SSH protocols.'
    )

    parser.add_argument(
        '--sshp-host',
        default=None,
        required=False,
        help='The host to netcat to when using `sshp://`, defaults to "localhost".'
    )

    args = parser.parse_args()

    kwargs = {}

    if args.timeout is not None:
        kwargs['timeout'] = args.timeout

    if args.verbose:
        kwargs['verbose'] = True

    if args.ssh_backend is not None:
        kwargs['ssh_backend'] = args.ssh_backend

    if args.ssh_port is not None:
        kwargs['ssh_port'] = args.ssh_port

    if args.sshp_host is not None:
        kwargs['sshp_host'] = args.sshp_host

    print('Connecting to:', args.url)
    c = Connection(args.url, **kwargs)
    c.tdic()
    c.disconnect()

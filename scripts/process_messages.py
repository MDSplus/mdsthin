
import os
import sys
import glob

from xml.etree import ElementTree

if len(sys.argv) < 2:
    print('process_messages.py PATH_TO_MDSPLUS_SOURCE')

mdsplus_source_path = sys.argv[1]
xml_filename_list = glob.glob(os.path.join(mdsplus_source_path, '**', '*_messages.xml'))

root_path = os.path.dirname(os.path.dirname(__file__))
source_path = os.path.join(root_path, 'mdsthin')
output_filename = os.path.join(source_path, 'exceptions.py')

SEVERITY_MAP = {
    'warning': 0,
    'success': 1,
    'error': 2,
    'info': 3,
    'fatal': 4,
    'internal': 7
}

SEVERITY_CODES = ['W', 'S', 'E', 'I', 'F', '?', '?', '?']

SKIP_FACILITY_LIST = [ 'Ss', 'Mdsdcl', 'Cam' ]

output_file = open(output_filename, 'wt')
output_file.write('''#
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

EXCEPTION_MAP = {}
EXCEPTION_PREFIX_MAP = {}

def STATUS_OK(status):
    return (status & 1)

def STATUS_NOT_OK(status):
    return not (status & 1)

def STATUS_FACILITY(status):
    return (status >> 16)

def STATUS_MESSAGE(status):
    return (status >> 3) & 0b1111111111111

def STATUS_SEVERITY(status):
    return (status & 0b111)

def getException(status):
    return EXCEPTION_MAP.get(status, MdsException(f'Unknown status: {status}'))

def getExceptionFromError(error):
    if type(error) is str and error.startswith('%'):
        prefix = error.split(',', maxsplit=1)[0]
        return EXCEPTION_PREFIX_MAP.get(prefix, MdsException(error))

    return MdsException(error)

class MdsException(Exception):
    pass

''')

for xml_filename in xml_filename_list:
    with open(xml_filename, 'rt') as xml_file:
        try:
            root = ElementTree.parse(xml_filename).getroot()
            for facility in root.iter('facility'):
                facility_name = facility.get('name')
                facility_value = int(facility.get('value'))

                if facility_name in SKIP_FACILITY_LIST:
                    continue

                output_file.write(f'class {facility_name}Exception(MdsException):\n')
                output_file.write(f'    pass\n')
                output_file.write('\n')

                for status in facility.iter('status'):
                    status_name = status.get('name')
                    status_value = int(status.get('value'))

                    if status_name.startswith('CAM_') or status_name == 'CAMACERR':
                        continue

                    facility_name_override = status.get('facnam')
                    facility_abbreviation = status.get('facabb', facility_name)
                    if facility_name_override is not None:
                        continue

                    deprecated = status.get('deprecated', None)
                    if deprecated is not None:
                        continue

                    severity = SEVERITY_MAP[status.get('severity').lower()]

                    message = status.get('text', None)
                    if message is None:
                        continue

                    message = message.replace('  ', ' ')
                    message = message[0].upper() + message[ 1 : ]
                    if message[-1] == '.':
                        message = message[ : -1 ]

                    message_name = facility_name + status_name
                    message_value = (facility_value << 16) + (status_value << 3) + severity
                    message_prefix = f'%{facility_name.upper()}-{SEVERITY_CODES[severity]}-{status_name.upper()}'

                    output_file.write(f'class {message_name}({facility_name}Exception):\n')
                    output_file.write(f'    status = {message_value}\n')
                    output_file.write(f'    prefix = "{message_prefix}"\n')
                    output_file.write(f'    def __init__(self):\n')
                    output_file.write(f'        Exception.__init__(self, "{message_prefix}, {message}")\n')
                    output_file.write('\n')
                    output_file.write(f'EXCEPTION_MAP[{message_name}.status] = {message_name}\n')
                    output_file.write(f'EXCEPTION_PREFIX_MAP[{message_name}.prefix] = {message_name}\n')
                    output_file.write('\n')

        except Exception as e:
            print(e)
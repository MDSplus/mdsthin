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

#
# This package provdes a "best effort" approach to adding compatability with the real MDSplus Python package
# Several classes are similar but with different names, others are missing entirely. So we map what we can,
# and can provide additional compatability mapping in the future
#

from ..connection import Connection, GetMany, PutMany

from ..descriptors import String, StringArray
from ..descriptors import Int8, Int16, Int32, Int64, Int8Array, Int16Array, Int32Array, Int64Array
from ..descriptors import List, Dictionary
from ..descriptors import Signal, Dimension, Window, Slope, Function, Conglom, Range, Action, Dispatch
from ..descriptors import Program, Routine, Procedure, Method, Dependency, Condition, WithUnits, Call, WithError
from ..functions import *

# Compatability

del Connection.tcl
del Connection.tdic
del Connection.mdstcl

@property
def hostspec(self):
    return self._url

Connection.hostspec = hostspec

from ..descriptors import Descriptor as Data
from ..descriptors import Descriptor as DescriptorNULL
from ..descriptors import Descriptor as EmptyData

from ..descriptors import UInt8 as Uint8
from ..descriptors import UInt16 as Uint16
from ..descriptors import UInt32 as Uint32
from ..descriptors import UInt64 as Uint64

from ..descriptors import UInt8Array as Uint8Array
from ..descriptors import UInt16Array as Uint16Array
from ..descriptors import UInt32Array as Uint32Array
from ..descriptors import UInt64Array as Uint64Array

from .. import exceptions as mdsExceptions

mdsExceptions.statusToException = mdsExceptions.getException

def checkStatus(status, ignore=tuple(), message=None):
    # TODO: message
    if mdsExceptions.STATUS_NOT_OK(status):
        exception = mdsExceptions.getException(status)
        if isinstance(exception, ignore):
            print(exception)
        else:
            raise exception
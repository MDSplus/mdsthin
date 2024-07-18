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
import numpy

from .dtypedef import *

###
### VMS
###

class F_Floating(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('fraction', ctypes.c_uint32, 7),
        ('exponent', ctypes.c_uint32, 8),
        ('sign', ctypes.c_uint32, 1),
        ('fraction2', ctypes.c_uint32, 16),
    ]

class D_Floating(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('fraction', ctypes.c_uint64, 7),
        ('exponent', ctypes.c_uint64, 8),
        ('sign', ctypes.c_uint64, 1),
        ('fraction2', ctypes.c_uint64, 16),
        ('fraction3', ctypes.c_uint64, 16),
        ('fraction4', ctypes.c_uint64, 16),
    ]

class G_Floating(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('fraction', ctypes.c_uint64, 4),
        ('exponent', ctypes.c_uint64, 11),
        ('sign', ctypes.c_uint64, 1),
        ('fraction2', ctypes.c_uint64, 16),
        ('fraction3', ctypes.c_uint64, 16),
        ('fraction4', ctypes.c_uint64, 16),
    ]

class H_Floating(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('exponent', ctypes.c_uint64, 15),
        ('sign', ctypes.c_uint64, 1),
        ('fraction', ctypes.c_uint64, 16),
        ('fraction2', ctypes.c_uint64, 16),
        ('fraction3', ctypes.c_uint64, 16),
        ('fraction4', ctypes.c_uint64, 16),
        ('fraction5', ctypes.c_uint64, 16),
        ('fraction6', ctypes.c_uint64, 16),
        ('fraction7', ctypes.c_uint64, 16),
    ]

###
### IEEE
###

class IEEE_Single(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('mantissa', ctypes.c_uint32, 23),
        ('exponent', ctypes.c_uint32, 8),
        ('sign', ctypes.c_uint32, 1),
    ]

class IEEE_Double(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('mantissa', ctypes.c_uint64, 52),
        ('exponent', ctypes.c_uint64, 11),
        ('sign', ctypes.c_uint64, 1),
    ]

class IEEE_LongDouble(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('mantissa', ctypes.c_uint64, 64),
        ('mantissa2', ctypes.c_uint64, 48),
        ('exponent', ctypes.c_uint64, 15),
        ('sign', ctypes.c_uint64, 1),
    ]

###
### Unions
###

class Float(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ('F', F_Floating),
        ('FS', IEEE_Single),
        ('value', ctypes.c_float),
    ]

    def convert_F(self):
        
        sign = self.F.sign
        exponent = self.F.exponent - 128
        fraction = (
            (self.F.fraction << 16) |
            self.F.fraction2
        )

        self.FS.sign = sign
        self.FS.exponent = exponent + 126
        self.FS.mantissa = fraction

        return self.value

class Double(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ('D', D_Floating),
        ('G', G_Floating),
        ('FT', IEEE_Double),
        ('value', ctypes.c_double),
    ]

    def convert_D(self):
        
        sign = self.D.sign
        fraction = ((self.D.fraction << 48)
                    | (self.D.fraction2 << 32)
                    | (self.D.fraction3 << 16)
                    | self.D.fraction4)
        exponent = self.D.exponent - 128

        # TODO: What the fuck

        self.FT.sign = sign
        self.FT.exponent = exponent + 1022
        self.FT.mantissa = fraction

        return self.value

    def convert_G(self):

        sign = self.G.sign
        fraction = ((self.G.fraction << 48)
                    | (self.G.fraction2 << 32)
                    | (self.G.fraction3 << 16)
                    | self.G.fraction4)
        exponent = self.G.exponent - 1024

        self.FT.sign = sign
        self.FT.exponent = exponent + 1022
        self.FT.mantissa = fraction

        return self.value
    
class LongDouble(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ('H', H_Floating),
        ('FQ', IEEE_LongDouble),
        ('value', ctypes.c_longdouble),
    ]

    def convert_H(self):

        sign = self.H.sign
        # fraction = (self.H.fraction << 48) | (self.H.fraction2 << 32) | (self.H.fraction3 << 16) | self.H.fraction4
        # fraction2 = (self.H.fraction5 << 32) | (self.H.fraction6 << 16) | self.H.fraction7
        fraction = ((self.H.fraction << 96)
                    | (self.H.fraction2 << 80)
                    | (self.H.fraction3 << 64)
                    | (self.H.fraction4 << 48)
                    | (self.H.fraction5 << 32)
                    | (self.H.fraction6 << 16)
                    | self.H.fraction7)
        exponent = self.H.exponent - 1024

        self.FQ.sign = sign
        self.FQ.exponent = exponent + 1022
        self.FQ.mantissa = (fraction >> 48)
        self.FQ.mantissa2 = (fraction & 0xFFFFFF)

        return self.value

def convert_float(dtype, buffer):

    if dtype == DTYPE_F:
        return numpy.float32(Float.from_buffer(buffer).convert_F())

    elif dtype == DTYPE_D:
        return numpy.float64(Double.from_buffer(buffer).convert_D())

    elif dtype == DTYPE_G:
        return numpy.float64(Double.from_buffer(buffer).convert_G())

    elif dtype == DTYPE_H:
        # not supported
        # return numpy.float128(LongDouble.from_buffer(buffer).convert_H())
        return None

def convert_float_array(dtype, buffer):

    if dtype == DTYPE_F:
        length = len(buffer) // ctypes.sizeof(Float)
        items = (Float * length).from_buffer(buffer)
        return numpy.array([ item.convert_F() for item in items ], dtype=numpy.float32)
    
    elif dtype == DTYPE_D:
        length = len(buffer) // ctypes.sizeof(Double)
        items = (Double * length).from_buffer(buffer)
        return numpy.array([ item.convert_D() for item in items ], dtype=numpy.float64)
    
    elif dtype == DTYPE_G:
        length = len(buffer) // ctypes.sizeof(Double)
        items = (Double * length).from_buffer(buffer)
        return numpy.array([ item.convert_G() for item in items ], dtype=numpy.float64)
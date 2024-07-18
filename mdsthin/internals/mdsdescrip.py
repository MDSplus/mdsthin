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

from .dtypedef import *
from .classdef import *

###
### mdsdsc_t
###

class mdsdsc_t(ctypes.LittleEndianStructure):
    """
    Descriptor base class
    """

    _pack_ = 1
    _fields_ = [
        ('length', ctypes.c_uint16),
        ('dtype_id', dtype_t),
        ('class_id', class_t),
        ('offset', ctypes.c_uint32), # pointer
    ]

    @property
    def class_str(self):
        return class_to_string(self.class_id)
    
    @property
    def dtype_str(self):
        return dtype_to_string(self.dtype_id)

###
### mdsdsc_s_t
###

class mdsdsc_s_t(mdsdsc_t):
    """
    Static fixed-length descriptor (CLASS_S)
    """

###
### mdsdsc_d_t
###

class mdsdsc_d_t(mdsdsc_t):
    """
    Dynamic string descriptor (CLASS_D)
    """

###
### mdsdsc_a_t
###

class aflags_t(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('fill', ctypes.c_uint8, 3),
        ('binscale', ctypes.c_uint8, 1),
        ('redim', ctypes.c_uint8, 1),
        ('column', ctypes.c_uint8, 1),
        ('coeff', ctypes.c_uint8, 1),
        ('bounds', ctypes.c_uint8, 1),
    ]

class mdsdsc_a_t(mdsdsc_t):
    """
    Array descriptor (CLASS_A, CLASS_CA, CLASS_APD)
    """

    _pack_ = 1
    _fields_ = [
        ('scale', ctypes.c_int8),
        ('digits', ctypes.c_uint8),
        ('aflags', aflags_t),
        ('dimct', ctypes.c_uint8),
        ('arsize', ctypes.c_uint32),
    ]

###
### mdsdsc_r_t
###

class mdsdsc_r_t(mdsdsc_t):
    """
    Record descriptor (CLASS_R)
    """
    
    _pack_ = 1
    _fields_ = [
        ('ndesc', ctypes.c_uint32, 8),
        ('fill', ctypes.c_uint32, 24),
    ]

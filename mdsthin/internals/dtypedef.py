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

###
### dtype_t
###

dtype_t = ctypes.c_ubyte

DTYPE_MISSING = 0
"""No data"""

DTYPE_V = 1
"""(deprecated) Aligned bit string"""

DTYPE_BU = 2
"""Byte Unsigned, 8-bit unsigned integer"""

DTYPE_WU = 3
"""Word Unsigned, 16-bit unsigned integer"""

DTYPE_LU = 4
"""Long Unsigned, 32-bit integer"""

DTYPE_QU = 5
"""Quadword Unsigned, 64-bit integer"""

DTYPE_B = 6
"""Byte, 8-bit signed integer"""

DTYPE_W = 7
"""Word, 16-bit signed integer"""

DTYPE_L = 8
"""Long 32-bit signed integer"""

DTYPE_Q = 9
"""Quadword 64-bit signed integer"""

DTYPE_F = 10
"""(deprecated) VMS F_Floating 32-bit single-precision floating point"""

DTYPE_D = 11
"""(deprecated) VMS D_Floating 64-bit single-precision floating point"""

DTYPE_FC = 12
"""(deprecated) DTYPE_F Complex"""

DTYPE_DC = 13
"""(deprecated) DTYPE_D Complex"""

DTYPE_T = 14
"""Text, ASCII 8-bit character string"""

DTYPE_DSC = 24
"""Descriptor"""

DTYPE_OU = 25
"""Octaword Unsigned, 128-bit unsigned integer"""

DTYPE_O = 26
"""Unsigned Octaword, 128-bit signed integer"""

DTYPE_G = 27
"""(deprecated) VMS G_floating 64-bit double-precision floating point"""

DTYPE_H = 28
"""(deprecated) VMS H_Floating 128-bit quadruple-precision floating point"""

DTYPE_GC = 29
"""(deprecated) DTYPE_G complex"""

DTYPE_HC = 30
"""(deprecated) DTYPE_H complex"""

DTYPE_POINTER = 51
"""TODO: """

DTYPE_FS = 52
"""IEEE 32-bit single-precision floating point"""

DTYPE_FT = 53
"""IEEE 64-bit double-precision floating point"""

DTYPE_FSC = 54
"""DTYPE_FS complex"""

DTYPE_FTC = 55
"""DTYPE_FT complex"""

DTYPE_C = 56
"""Used for char* returned by TdiCall() that must be freed"""

DTYPE_IDENT = 191
"""TODO: """

DTYPE_NID = 192
"""Node identification number, see NID"""

DTYPE_PATH = 193
"""Path to node as a string"""

DTYPE_PARAM = 194
"""TODO: """

DTYPE_SIGNAL = 195
"""Signal()"""

DTYPE_DIMENSION = 196
"""Dimension()"""

DTYPE_WINDOW = 197
"""Window()"""

DTYPE_SLOPE = 198
"""Slope()"""

DTYPE_FUNCTION = 199
"""TODO: """

DTYPE_CONGLOM = 200
"""TODO: """

DTYPE_RANGE = 201
"""Range()"""

DTYPE_ACTION = 202
"""Action()"""

DTYPE_DISPATCH = 203
"""Dispatch()"""

DTYPE_PROGRAM = 204
"""(deprecated) TODO: """

DTYPE_ROUTINE = 205
"""(deprecated) TODO: """

DTYPE_PROCEDURE = 206
"""(deprecated) TODO: """

DTYPE_METHOD = 207
"""Method()"""

DTYPE_DEPENDENCY = 208
"""TODO: """

DTYPE_CONDITION = 209
"""TODO: """

DTYPE_EVENT = 210
"""TODO: """

DTYPE_WITH_UNITS = 211
"WithUnits()"

DTYPE_CALL = 212
"""TODO: """

DTYPE_WITH_ERROR = 213
"""WithError()"""

DTYPE_LIST = 214
"""List()"""

DTYPE_TUPLE = 215
"""TODO: """

DTYPE_DICTIONARY = 216
"""TODO: """

DTYPE_OPAQUE = 217
"""TODO: """

NUMERIC_DTYPES = [
    DTYPE_BU, DTYPE_WU, DTYPE_LU, DTYPE_QU,
    DTYPE_B, DTYPE_W, DTYPE_L, DTYPE_Q,
    DTYPE_F, DTYPE_D, DTYPE_FC, DTYPE_DC,
    DTYPE_OU, DTYPE_O,
    DTYPE_G, DTYPE_H, DTYPE_GC, DTYPE_HC,
    DTYPE_FS, DTYPE_FT, DTYPE_FSC, DTYPE_FTC,
    DTYPE_DSC,
]

def dtype_is_numeric(dtype_id) -> bool:
    if type(dtype_id) is dtype_t:
        dtype_id = dtype_id.value

    return dtype_id in NUMERIC_DTYPES

EXPRESSION_DTYPES = [
    DTYPE_FUNCTION,
    DTYPE_NID,
    DTYPE_PATH,
    DTYPE_IDENT,
    DTYPE_CALL
]

def dtype_is_expression(dtype_id) -> bool:
    if type(dtype_id) is dtype_t:
        dtype_id = dtype_id.value

    return dtype_id in EXPRESSION_DTYPES

def dtype_to_string(dtype_id) -> str:
    VALUES = {
        DTYPE_MISSING: 'DTYPE_MISSING',
        DTYPE_V: 'DTYPE_V',
        DTYPE_BU: 'DTYPE_BU',
        DTYPE_WU: 'DTYPE_WU',
        DTYPE_LU: 'DTYPE_LU',
        DTYPE_QU: 'DTYPE_QU',
        DTYPE_B: 'DTYPE_B',
        DTYPE_W: 'DTYPE_W',
        DTYPE_L: 'DTYPE_L',
        DTYPE_Q: 'DTYPE_Q',
        DTYPE_F: 'DTYPE_F',
        DTYPE_D: 'DTYPE_D',
        DTYPE_FC: 'DTYPE_FC',
        DTYPE_DC: 'DTYPE_DC',
        DTYPE_T: 'DTYPE_T',
        DTYPE_DSC: 'DTYPE_DSC',
        DTYPE_OU: 'DTYPE_OU',
        DTYPE_O: 'DTYPE_O',
        DTYPE_G: 'DTYPE_G',
        DTYPE_H: 'DTYPE_H',
        DTYPE_GC: 'DTYPE_GC',
        DTYPE_HC: 'DTYPE_HC',
        DTYPE_POINTER: 'DTYPE_POINTER',
        DTYPE_FS: 'DTYPE_FS',
        DTYPE_FT: 'DTYPE_FT',
        DTYPE_FSC: 'DTYPE_FSC',
        DTYPE_FTC: 'DTYPE_FTC',
        DTYPE_C: 'DTYPE_C',
        DTYPE_IDENT: 'DTYPE_IDENT',
        DTYPE_NID: 'DTYPE_NID',
        DTYPE_PATH: 'DTYPE_PATH',
        DTYPE_PARAM: 'DTYPE_PARAM',
        DTYPE_SIGNAL: 'DTYPE_SIGNAL',
        DTYPE_DIMENSION: 'DTYPE_DIMENSION',
        DTYPE_WINDOW: 'DTYPE_WINDOW',
        DTYPE_SLOPE: 'DTYPE_SLOPE',
        DTYPE_FUNCTION: 'DTYPE_FUNCTION',
        DTYPE_CONGLOM: 'DTYPE_CONGLOM',
        DTYPE_RANGE: 'DTYPE_RANGE',
        DTYPE_ACTION: 'DTYPE_ACTION',
        DTYPE_DISPATCH: 'DTYPE_DISPATCH',
        DTYPE_PROGRAM: 'DTYPE_PROGRAM',
        DTYPE_ROUTINE: 'DTYPE_ROUTINE',
        DTYPE_PROCEDURE: 'DTYPE_PROCEDURE',
        DTYPE_METHOD: 'DTYPE_METHOD',
        DTYPE_DEPENDENCY: 'DTYPE_DEPENDENCY',
        DTYPE_CONDITION: 'DTYPE_CONDITION',
        DTYPE_EVENT: 'DTYPE_EVENT',
        DTYPE_WITH_UNITS: 'DTYPE_WITH_UNITS',
        DTYPE_CALL: 'DTYPE_CALL',
        DTYPE_WITH_ERROR: 'DTYPE_WITH_ERROR',
        DTYPE_LIST: 'DTYPE_LIST',
        DTYPE_TUPLE: 'DTYPE_TUPLE',
        DTYPE_DICTIONARY: 'DTYPE_DICTIONARY',
        DTYPE_OPAQUE: 'DTYPE_OPAQUE',
    }

    if type(dtype_id) is dtype_t:
        dtype_id = dtype_id.value

    if dtype_id in VALUES:
        return VALUES[dtype_id]

    return f'DTYPE_UNKNOWN({dtype_id})'

def get_dtype_size(dtype_id) -> int:
    if type(dtype_id) is dtype_t:
        dtype_id = dtype_id.value

    if dtype_id in [ DTYPE_BU, DTYPE_B ]:
        return 1
    if dtype_id in [ DTYPE_WU, DTYPE_W ]:
        return 2
    if dtype_id in [ DTYPE_LU, DTYPE_L, DTYPE_F, DTYPE_FS ]:
        return 4
    if dtype_id in [ DTYPE_QU, DTYPE_Q, DTYPE_D, DTYPE_G, DTYPE_FT ]:
        return 8
    if dtype_id in [ DTYPE_OU, DTYPE_O ]:
        return 16
    
    return 0
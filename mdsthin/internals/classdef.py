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
### class_t
###

class_t = ctypes.c_ubyte

CLASS_MISSING = 0
"""Invalid class"""

CLASS_S = 1
"""`S`tatic fixed-length descriptor"""

CLASS_D = 2
"""`D`ynamic string descriptor"""

CLASS_V = 3
"""(deprecated) VMS `V`ariable buffer descriptor"""

CLASS_A = 4
"""`A`rray descriptor"""

CLASS_P = 5
"""(deprecated?) Procedure descriptor"""

CLASS_PI = 6
"""(deprecated?) Procedure incarnation descriptor"""

CLASS_J = 7
"""(deprecated) VMS debugger label descriptor"""

CLASS_JI = 8
"""(deprecated) VMS debugger label incarnation descriptor"""

CLASS_SD = 9
"""(deprecated?) Decimal string descriptor"""

CLASS_NCA = 10
"""(deprecated?) `N`on`c`ontiguous `A`rray descriptor"""

CLASS_VS = 11
"""(deprecated?) `V`arying `S`tring descriptor"""

CLASS_VSA = 12
"""(deprecated?) `V`arying `S`tring `A`rray descriptor"""

CLASS_UBS = 13
"""(deprecated?) `U`naligned `B`it `S`tring descriptor"""

CLASS_UBA = 14
"""(deprecated?) `U`naligned `B`it `A`rray descriptor"""

CLASS_SB = 15
"""(deprecated?) `S`tring with `B`ounds descriptor"""

CLASS_UBSB = 16
"""(deprecated?) `U`naligned `B`it `S`tring with `B`ounds descriptor"""

CLASS_XD = 192
"""E`x`tended `D`ynamic descriptor"""

CLASS_XS = 193
"""E`x`tended `S`tatic descriptor"""

CLASS_R = 194
"""`R`ecord descriptor"""

CLASS_CA = 195
"""`C`ompressed `A`rray descriptor"""

CLASS_APD = 196
"""`A`rray of `P`ointers to `D`ata descriptor"""

ARRAY_CLASSES = [
    CLASS_A,
    CLASS_CA,
    CLASS_APD,
]

def class_is_array(class_id) -> bool:
    if type(class_id) is class_t:
        class_id = class_id.value

    return class_id in ARRAY_CLASSES

def class_to_string(class_id) -> str:
    VALUES = {
        CLASS_MISSING: 'CLASS_MISSING',
        CLASS_S: 'CLASS_S',
        CLASS_D: 'CLASS_D',
        CLASS_V: 'CLASS_V',
        CLASS_A: 'CLASS_A',
        CLASS_P: 'CLASS_P',
        CLASS_PI: 'CLASS_PI',
        CLASS_J: 'CLASS_J',
        CLASS_JI: 'CLASS_JI',
        CLASS_SD: 'CLASS_SD',
        CLASS_NCA: 'CLASS_NCA',
        CLASS_VS: 'CLASS_VS',
        CLASS_VSA: 'CLASS_VSA',
        CLASS_UBS: 'CLASS_UBS',
        CLASS_UBA: 'CLASS_UBA',
        CLASS_SB: 'CLASS_SB',
        CLASS_UBSB: 'CLASS_UBSB',
        CLASS_XD: 'CLASS_XD',
        CLASS_XS: 'CLASS_XS',
        CLASS_R: 'CLASS_R',
        CLASS_CA: 'CLASS_CA',
        CLASS_APD: 'CLASS_APD',
    }

    if type(class_id) is class_t:
        class_id = class_id.value

    if class_id in VALUES:
        return VALUES[class_id]

    return f'CLASS_UNKNOWN({class_id})'

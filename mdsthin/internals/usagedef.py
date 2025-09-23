#
# Copyright (c) 2025, Massachusetts Institute of Technology All rights reserved.
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
### usage_t
###

usage_t = ctypes.c_byte

TreeUSAGE_ANY = 0
"""Node could contain anything"""

TreeUSAGE_STRUCTURE = 1
"""Node should not contain data and will be used as a directory"""

TreeUSAGE_ACTION = 2
"""
Node should contain an Action()

dtype = `DTYPE_ACTION` or one of `EXPRESSION_DTYPES`
"""

TreeUSAGE_DEVICE = 3
"""
Node will be treated as the head of a Device

dtype = `DTYPE_CONGLOM`
"""

TreeUSAGE_DISPATCH = 4
"""
Node should contain a Dispatch()

dtype = `DTYPE_DISPATCH` or one of `EXPRESSION_DTYPES`
"""

TreeUSAGE_NUMERIC = 5
"""
Node should contain numeric data

dtype = one of `NUMERIC_DTYPES` or `DTYPE_PARAM` or `DTYPE_RANGE` or `DTYPE_WITH_UNITS` or `DTYPE_WITH_ERROR` or `DTYPE_OPAQUE` or one of `EXPRESSION_DTYPES`
"""

TreeUSAGE_SIGNAL = 6
"""
Node should contain a Signal()

dtype = `DTYPE_SIGNAL` or one of `EXPRESSION_DTYPES`
"""

TreeUSAGE_TASK = 7
"""
Node should contain a Task

dtype = `DTYPE_PROGRAM` or `DTYPE_ROUTINE` or `DTYPE_PROCEDURE` or `DTYPE_METHOD` or one of `EXPRESSION_DTYPES`
"""

TreeUSAGE_TEXT = 8
"""
Node should contain text

dtype = `DTYPE_T` or `DTYPE_PARAM` or `DTYPE_WITH_UNITS` or `DTYPE_OPAQUE` or `DTYPE_DSC` or one of `EXPRESSION_DTYPES`
"""

TreeUSAGE_WINDOW = 9
"""
Node should contain a Window()

dtype = `DTYPE_WINDOW` or one of `EXPRESSION_DTYPES`
"""

TreeUSAGE_AXIS = 10
"""
Node should contain TODO: ???

dtype = one of `NUMERIC_TYPES` or `DTYPE_SLOPE` or `DTYPE_RANGE` or `DTYPE_WITH_UNITS` or `DTYPE_DIMENSION` or one of `EXPRESSION_TYPES`
"""

TreeUSAGE_SUBTREE = 11
"""
Node should not contain data and will be treated as a subtree
"""

TreeUSAGE_COMPOUND_DATA = 12
"""
Node should contain a compound data type

dtype = `DTYPE_CONGLOM`
"""

TreeUSAGE_MAXIMUM = TreeUSAGE_COMPOUND_DATA + 1
"""The number of values of usage_t"""

TreeUSAGE_SUBTREE_REF = TreeUSAGE_MAXIMUM + 1
"""TODO: """

TreeUSAGE_SUBTREE_TOP = TreeUSAGE_SUBTREE_REF + 1
"""TODO: """

def usage_lookup(name):
    table = {
        'ANY': TreeUSAGE_ANY,
        'NONE': TreeUSAGE_STRUCTURE,
        'STRUCTURE': TreeUSAGE_STRUCTURE,
        'ACTION': TreeUSAGE_ACTION,
        'DEVICE': TreeUSAGE_DEVICE,
        'DISPATCH': TreeUSAGE_DISPATCH,
        'NUMERIC': TreeUSAGE_NUMERIC,
        'SIGNAL': TreeUSAGE_SIGNAL,
        'TASK': TreeUSAGE_TASK,
        'TEXT': TreeUSAGE_TEXT,
        'WINDOW': TreeUSAGE_WINDOW,
        'AXIS': TreeUSAGE_AXIS,
        'SUBTREE': TreeUSAGE_SUBTREE,
        'COMPOUND_DATA': TreeUSAGE_COMPOUND_DATA,
    }

    return table[name.upper()]

def usage_to_string(usage: usage_t | int) -> str:
    VALUES = {
        TreeUSAGE_ANY: 'TreeUSAGE_ANY',
        TreeUSAGE_STRUCTURE: 'TreeUSAGE_STRUCTURE',
        TreeUSAGE_ACTION: 'TreeUSAGE_ACTION',
        TreeUSAGE_DEVICE: 'TreeUSAGE_DEVICE',
        TreeUSAGE_DISPATCH: 'TreeUSAGE_DISPATCH',
        TreeUSAGE_NUMERIC: 'TreeUSAGE_NUMERIC',
        TreeUSAGE_SIGNAL: 'TreeUSAGE_SIGNAL',
        TreeUSAGE_TASK: 'TreeUSAGE_TASK',
        TreeUSAGE_TEXT: 'TreeUSAGE_TEXT',
        TreeUSAGE_WINDOW: 'TreeUSAGE_WINDOW',
        TreeUSAGE_AXIS: 'TreeUSAGE_AXIS',
        TreeUSAGE_SUBTREE: 'TreeUSAGE_SUBTREE',
        TreeUSAGE_COMPOUND_DATA: 'TreeUSAGE_COMPOUND_DATA',
        TreeUSAGE_MAXIMUM: 'TreeUSAGE_MAXIMUM',
        TreeUSAGE_SUBTREE_REF: 'TreeUSAGE_SUBTREE_REF',
        TreeUSAGE_SUBTREE_TOP: 'TreeUSAGE_SUBTREE_TOP',
    }

    if type(usage) is usage_t:
        usage = usage.value

    if usage in VALUES:
        return VALUES[usage]

    return f'TreeUSAGE_UNKNOWN({usage})'

def usage_to_name(usage: usage_t | int) -> str:
    return usage_to_string(usage).removeprefix('TreeUSAGE_')
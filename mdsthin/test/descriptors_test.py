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

import numpy
import unittest

from ..descriptors import *

class DescriptorsTest(unittest.TestCase):

    def test_integer_limits(self):

        tests = [
            { 'type': UInt8,  'min': 0, 'max': numpy.iinfo(numpy.uint8).max },
            { 'type': UInt16, 'min': 0, 'max': numpy.iinfo(numpy.uint16).max },
            { 'type': UInt32, 'min': 0, 'max': numpy.iinfo(numpy.uint32).max },
            { 'type': UInt64, 'min': 0, 'max': numpy.iinfo(numpy.uint64).max },

            { 'type': Int8,  'min': numpy.iinfo(numpy.int8).min,  'max': numpy.iinfo(numpy.int8).max },
            { 'type': Int16, 'min': numpy.iinfo(numpy.int16).min, 'max': numpy.iinfo(numpy.int16).max },
            { 'type': Int32, 'min': numpy.iinfo(numpy.int32).min, 'max': numpy.iinfo(numpy.int32).max },
            { 'type': Int64, 'min': numpy.iinfo(numpy.int64).min, 'max': numpy.iinfo(numpy.int64).max },
        ]

        for info in tests:
            name = repr(info['type'])
            with self.subTest(name):

                data = info['type'](info['min'])
                self.assertEqual(type(data), info['type'])
                self.assertEqual(data.data(), info['min'])

                data = info['type'](info['min'])
                self.assertEqual(type(data), info['type'])
                self.assertEqual(data.data(), info['min'])

                data = info['type'](42)
                self.assertEqual(type(data), info['type'])
                self.assertEqual(data.data(), 42)

    def test_string(self):

        string = 'Hello, World!'
        data = String(string)
        self.assertEqual(type(data), String)
        self.assertEqual(data.data(), string)

        string = 'a' * 1048576 # 1MB
        data = String(string)
        self.assertEqual(type(data), String)
        self.assertEqual(data.data(), string)

        data = String()
        self.assertEqual(type(data), String)
        self.assertEqual(data.data(), '')

        self.assertRaises(UnicodeEncodeError, String, '🔥')

        buffer = '🔥'.encode()
        self.assertRaises(UnicodeDecodeError, String.unpack_data, buffer)

    def test_string_array(self):
        
        strings = ['a', 'b', 'c']
        data = StringArray(strings)
        self.assertEqual(type(data), StringArray)
        self.assertEqual(data, numpy.array(strings, dtype=str))
        self.assertTrue((data.data_raw() == ['a', 'b', 'c']).all())
        
        strings = ['one', 'seven', 'nineteen']
        data = StringArray(strings)
        self.assertEqual(type(data), StringArray)
        self.assertEqual(data, numpy.array(strings, dtype=str))
        self.assertTrue((data.data_raw() == ['one     ', 'seven   ', 'nineteen']).all())
        
        strings = [ ['one', 'two'], ['three', 'four'] ]
        data = StringArray(strings)
        self.assertEqual(type(data), StringArray)
        self.assertEqual(data, numpy.array(strings, dtype=str))
        self.assertTrue((data.data_raw() == [ ['one  ', 'two  '], ['three', 'four '] ]).all())

    def test_native_types(self):

        data = Descriptor('test')
        self.assertEqual(type(data), String)
        self.assertEqual(data, 'test')
        
        data = Descriptor(True)
        self.assertEqual(type(data), UInt8)
        self.assertEqual(data, True)

        data = Descriptor(42)
        self.assertEqual(type(data), Int64)
        self.assertEqual(data, 42)
        
        data = Descriptor(3.14159)
        self.assertEqual(type(data), Float64)
        self.assertEqual(data, 3.14159)
        
        data = Descriptor(b'\xCA\xFE')
        self.assertEqual(type(data), UInt8Array)
        self.assertEqual(data, numpy.array([ 0xCA, 0xFE ], dtype=numpy.uint8))

        data = Descriptor(bytearray(b'\xCA\xFE'))
        self.assertEqual(type(data), UInt8Array)
        self.assertEqual(data, numpy.array([ 0xCA, 0xFE ], dtype=numpy.uint8))

        buffer = b'\xCA\xFE'
        data = Descriptor(memoryview(buffer))
        self.assertEqual(type(data), UInt8Array)
        self.assertEqual(data, numpy.array([ 0xCA, 0xFE ], dtype=numpy.uint8))

        items = [ 1, 'b', 3.0 ]
        data = Descriptor(items)
        self.assertEqual(type(data), List)
        self.assertEqual(type(data[0]), Int64)
        self.assertEqual(type(data[1]), String)
        self.assertEqual(type(data[2]), Float64)
        self.assertListEqual(data.data(), items)

        items = ( 1, 'b', 3.0 )
        data = Descriptor(items)
        self.assertEqual(type(data), Tuple)
        self.assertEqual(type(data[0]), Int64)
        self.assertEqual(type(data[1]), String)
        self.assertEqual(type(data[2]), Float64)
        self.assertTupleEqual(data.data(), items)

    def test_vms_floats(self):
        
        tests = [
            {
                'dtype': DTYPE_F,
                'buffer': bytearray([ 0x49, 0x41, 0xD0, 0x0F ]),
                'type': Float32,
                'value': 3.14159,
            },
            # {
            #     'dtype': DTYPE_FC,
            #     'buffer': bytes([ 0x23, 0xC6, 0xCD, 0x70 ]),
            #     'type': Float32,
            #     'value': 3.14159,
            # },
            # {
            #     'dtype': DTYPE_D,
            #     'buffer': bytes([ 0x49, 0x41, 0xCF, 0x0F, 0xDC, 0x80, 0x70, 0x33 ]),
            #     'type': Float64,
            #     'value': 3.14159,
            # },
            # {
            #     'dtype': DTYPE_DC,
            #     'buffer': bytes([ 0x49, 0x41, 0xCF, 0x0F, 0xDC, 0x80, 0x70, 0x33 ]),
            #     'type': Float64,
            #     'value': 3.14159,
            # },
            {
                'dtype': DTYPE_G,
                'buffer': bytes([ 0x29, 0x40, 0xF9, 0x21, 0x1B, 0xF0, 0x6E, 0x86 ]),
                'type': Float64,
                'value': 3.14159,
            },
            # {
            #     'dtype': DTYPE_H,
            #     'buffer': bytes([ 0x02, 0x40, 0x1F, 0x92, 0x01, 0x9F, 0x66, 0xB8, 0x00, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]),
            #     'type': Float128,
            #     'value': 3.14159,
            # },
        ]


        for info in tests:
            name = dtype_to_string(info['dtype'])
            with self.subTest(name):

                dsc = mdsdsc_s_t(
                    length=len(info['buffer']),
                    dtype_id=info['dtype'],
                    class_id=CLASS_S,
                )

                buffer = bytes(dsc) + info['buffer']
                data = Descriptor.unpack(buffer)
                self.assertEqual(type(data), info['type'])
                self.assertAlmostEqual(data.data(), info['value'], places=5)
        
    def test_numpy_types(self):

        INTEGER_ARRAY = [ [2, 4], [6, 8], [16, 32] ]
        FLOAT_ARRAY = [ [1.0, 1.5], [2.0, 2.5], [3.0, 3.5] ]

        tests = [
            { 'type': UInt8,        'value': numpy.uint8(42), },
            { 'type': UInt16,       'value': numpy.uint16(42), },
            { 'type': UInt32,       'value': numpy.uint32(42), },
            { 'type': UInt64,       'value': numpy.uint64(42), },
            { 'type': Int8,         'value': numpy.int8(42), },
            { 'type': Int16,        'value': numpy.int16(42), },
            { 'type': Int32,        'value': numpy.int32(42), },
            { 'type': Int64,        'value': numpy.int64(42), },
            { 'type': Float32,      'value': numpy.float32(3.14159), },
            { 'type': Float64,      'value': numpy.float64(3.14159), },

            { 'type': UInt8Array,   'value': numpy.array(INTEGER_ARRAY, dtype=numpy.uint8) },
            { 'type': UInt16Array,  'value': numpy.array(INTEGER_ARRAY, dtype=numpy.uint16) },
            { 'type': UInt32Array,  'value': numpy.array(INTEGER_ARRAY, dtype=numpy.uint32) },
            { 'type': UInt64Array,  'value': numpy.array(INTEGER_ARRAY, dtype=numpy.uint64) },
            { 'type': Int8Array,    'value': numpy.array(INTEGER_ARRAY, dtype=numpy.int8) },
            { 'type': Int16Array,   'value': numpy.array(INTEGER_ARRAY, dtype=numpy.int16) },
            { 'type': Int32Array,   'value': numpy.array(INTEGER_ARRAY, dtype=numpy.int32) },
            { 'type': Int64Array,   'value': numpy.array(INTEGER_ARRAY, dtype=numpy.int64) },
            { 'type': Float32Array, 'value': numpy.array(FLOAT_ARRAY,   dtype=numpy.float32) },
            { 'type': Float64Array, 'value': numpy.array(FLOAT_ARRAY,   dtype=numpy.float64) },

            # TODO: string
            # TODO: string array
        ]

        for info in tests:
            name = repr(info['value'].dtype)
            with self.subTest(name):

                data = Descriptor(info['value'])
                self.assertEqual(type(data), info['type'])
                self.assertEqual(data.data().dtype, info['value'].dtype)
                self.assertEqual(data, info['value'])

    def test_apd_types(self):

        # List

        data = List()
        self.assertEqual(data, list())
        self.assertEqual(data.data(), list())
        
        data = List(1, 2, 3)
        self.assertEqual(data, [1, 2, 3])
        self.assertEqual(data.data(), [1, 2, 3])
        
        data.append(4)
        self.assertEqual(data, [1, 2, 3, 4])
        self.assertEqual(data.data(), [1, 2, 3, 4])

        data[1] = 5
        self.assertEqual(data, [1, 5, 3, 4])
        self.assertEqual(data.data(), [1, 5, 3, 4])
        
        data = List([1, 2], [3, 4], [5, 6])
        self.assertEqual(data, [ [1, 2], [3, 4], [5, 6] ])
        self.assertEqual(data.data(), [ [1, 2], [3, 4], [5, 6] ])

        # Tuple

        data = Tuple()
        self.assertEqual(data, tuple())
        self.assertEqual(data.data(), tuple())
        
        data = Tuple(1, 2, 3)
        self.assertEqual(data, (1, 2, 3))
        self.assertEqual(data.data(), (1, 2, 3))

        # Dictionary

        data = Dictionary()
        self.assertEqual(data, dict())
        self.assertEqual(data.data(), dict())

        data = Dictionary({ 'a': 1, 'b': 2, 'c': 3 })
        self.assertEqual(data, { 'a': 1, 'b': 2, 'c': 3 })
        self.assertEqual(data.data(), { 'a': 1, 'b': 2, 'c': 3 })

        data = Dictionary(('a', 1), ('b', 2), ('c', 3))
        self.assertEqual(data, { 'a': 1, 'b': 2, 'c': 3 })
        self.assertEqual(data.data(), { 'a': 1, 'b': 2, 'c': 3 })
        
        data['d'] = 4
        self.assertEqual(data, { 'a': 1, 'b': 2, 'c': 3, 'd': 4 })
        self.assertEqual(data.data(), { 'a': 1, 'b': 2, 'c': 3, 'd': 4 })

        data['b'] = 5
        self.assertEqual(data, { 'a': 1, 'b': 5, 'c': 3, 'd': 4 })
        self.assertEqual(data.data(), { 'a': 1, 'b': 5, 'c': 3, 'd': 4 })

    def test_arrays(self):
        
        INTEGER_ARRAY = [ 2, 4, 6 ]
        FLOAT_ARRAY = [ 1.0, 1.1, 1.2 ]

        tests = [
            { 'value': UInt32Array(list(range(100))), 'length': 100 },

            { 'value': UInt8Array(INTEGER_ARRAY), 'length': 3 },
            { 'value': UInt16Array(INTEGER_ARRAY), 'length': 3 },
            { 'value': UInt32Array(INTEGER_ARRAY), 'length': 3 },
            { 'value': UInt64Array(INTEGER_ARRAY), 'length': 3 },
            { 'value': Int8Array(INTEGER_ARRAY), 'length': 3 },
            { 'value': Int16Array(INTEGER_ARRAY), 'length': 3 },
            { 'value': Int32Array(INTEGER_ARRAY), 'length': 3 },
            { 'value': Int64Array(INTEGER_ARRAY), 'length': 3 },
            { 'value': Float32Array(FLOAT_ARRAY), 'length': 3 },
            { 'value': Float64Array(FLOAT_ARRAY), 'length': 3 },

            { 'value': StringArray(['one', 'seven', 'nineteen']), 'length': 3 },
        ]

        for info in tests:
            name = repr(type(info['value'])) + f"({info['length']})"
            with self.subTest(name):

                self.assertEqual(len(info['value']), info['length'])

                data = info['value'].data()
                
                for i in range(info['length']):
                    self.assertEqual(info['value'][i], data[i])
                
                for a, b in zip(info['value'], data):
                    self.assertEqual(a, b)

    def test_record_types(self):

        # Signal

        data = Signal()
        self.assertEqual(data.value, None)
        self.assertEqual(data.raw, None)
        self.assertEqual(data.dimensions, [])
        self.assertEqual(data.data(), None)
        self.assertRaises(IndexError, data.dim_of)

        data = Signal('value', 'raw', 'dim0', 'dim1', 'dim2')
        self.assertEqual(data.value, 'value')
        self.assertEqual(data.raw, 'raw')
        self.assertListEqual(list(data.dimensions), ['dim0', 'dim1', 'dim2'])
        self.assertEqual(data.data(), 'value')
        self.assertEqual(data.dim_of(), 'dim0')
        self.assertEqual(data.dim_of(0), 'dim0')
        self.assertEqual(data.dim_of(1), 'dim1')
        self.assertEqual(data.dim_of(2), 'dim2')
        self.assertEqual(data.dim_of(-1), 'dim2')
        self.assertRaises(IndexError, data.dim_of, 3)

        data = Signal(None, 'raw', 'dim')
        self.assertEqual(data.value, None)
        self.assertEqual(data.raw, 'raw')
        self.assertListEqual(list(data.dimensions), ['dim'])
        self.assertEqual(data.data(), 'raw')
        self.assertEqual(data.dim_of(), 'dim')
        self.assertRaises(IndexError, data.dim_of, 1)

        # Dimension

        data = Dimension()
        self.assertEqual(data.window, None)
        self.assertEqual(data.axis, None)

        data = Dimension('window', 'axis')
        self.assertEqual(data.window, 'window')
        self.assertEqual(data.axis, 'axis')

        # TODO: Put in a realistic axis
        data = Dimension(Window(0, 10, 5), 'axis')
        self.assertEqual(data.window, Window(0, 10, 5))
        self.assertEqual(data.axis, 'axis')

        # Window

        data = Window()
        self.assertEqual(data.startidx, None)
        self.assertEqual(data.endingidx, None)
        self.assertEqual(data.value_at_idx0, None)

        data = Window('startidx', 'endingidx', 'value_at_idx0')
        self.assertEqual(data.startidx, 'startidx')
        self.assertEqual(data.endingidx, 'endingidx')
        self.assertEqual(data.value_at_idx0, 'value_at_idx0')

        # Slope

        data = Slope()
        self.assertEqual(data.segments, [])

        self.assertRaises(Exception, Slope, 'broken')
        self.assertRaises(Exception, Slope, 'broken1', 'broken2')

        data = Slope('slope', 'begin', 'ending')
        self.assertListEqual(list(data.segments), [('slope', 'begin', 'ending')])

        data = Slope('slope0', 'begin0', 'ending0', 'slope1', 'begin1', 'ending1')
        self.assertListEqual(list(data.segments), [('slope0', 'begin0', 'ending0'), ('slope1', 'begin1', 'ending1')])

        # Function

        data = Function()
        self.assertEqual(data.opcode, 0)
        self.assertEqual(data.arguments, [])

        data = Function(162, None, 'whoami') # TdiCompile("whoami()")
        self.assertEqual(data.opcode, 162)
        self.assertEqual(data.arguments, [None, 'whoami'])

        self.assertRaises(Exception, data.data)

        # Conglom

        data = Conglom()
        self.assertEqual(data.image, None)
        self.assertEqual(data.model, None)
        self.assertEqual(data.name, None)
        self.assertEqual(data.qualifiers, None)

        data = Conglom('image', 'model', 'name', 'qualifiers')
        self.assertEqual(data.image, 'image')
        self.assertEqual(data.model, 'model')
        self.assertEqual(data.name, 'name')
        self.assertEqual(data.qualifiers, 'qualifiers')

        # Range

        data = Range()
        self.assertEqual(data.begin, None)
        self.assertEqual(data.ending, None)
        self.assertEqual(data.deltaval, None)

        data = Range('begin', 'ending', 'deltaval')
        self.assertEqual(data.begin, 'begin')
        self.assertEqual(data.ending, 'ending')
        self.assertEqual(data.deltaval, 'deltaval')

        data = Range(0, 10, 1)
        self.assertEqual(data.data(), range(0, 10, 1))

        # Python range() only supports integers
        data = Range(0.0, 1.0, 0.1)
        self.assertRaises(TypeError, data.data)

        # Action

        data = Action()
        self.assertEqual(data.dispatch, None)
        self.assertEqual(data.task, None)
        self.assertEqual(data.errorlogs, None)
        self.assertEqual(data.completion_message, None)
        self.assertEqual(data.performance, None)

        data = Action('dispatch', 'task', 'errorlogs', 'completion_message', 'performance')
        self.assertEqual(data.dispatch, 'dispatch')
        self.assertEqual(data.task, 'task')
        self.assertEqual(data.errorlogs, 'errorlogs')
        self.assertEqual(data.completion_message, 'completion_message')
        self.assertEqual(data.performance, 'performance')

        data = Action(Dispatch(0, 'ANALYSIS', 'INIT', 999, ''), Function(162, None, 'DoAnalysis'), '', None, None)
        self.assertEqual(data.dispatch, Dispatch(0, 'ANALYSIS', 'INIT', 999, ''))
        self.assertEqual(data.task, Function(162, None, 'DoAnalysis'))
        self.assertEqual(data.errorlogs, '')
        self.assertEqual(data.completion_message, None)
        self.assertEqual(data.performance, None)

        # Dispatch

        data = Dispatch()
        self.assertEqual(data.treesched, 0)
        self.assertEqual(data.ident, None)
        self.assertEqual(data.phase, None)
        self.assertEqual(data.when, None)
        self.assertEqual(data.completion, None)

        # TreeSCHED_ASYNC = 1
        data = Dispatch(1, 'ident', 'phase', 'when', 'completion')
        self.assertEqual(data.treesched, 1)
        self.assertEqual(data.ident, 'ident')
        self.assertEqual(data.phase, 'phase')
        self.assertEqual(data.when, 'when')
        self.assertEqual(data.completion, 'completion')

        # Program

        data = Program()
        self.assertEqual(data.time_out, None)
        self.assertEqual(data.program, None)

        data = Program('time_out', 'program')
        self.assertEqual(data.time_out, 'time_out')
        self.assertEqual(data.program, 'program')

        # Routine

        data = Routine()
        self.assertEqual(data.time_out, None)
        self.assertEqual(data.image, None)
        self.assertEqual(data.routine, None)
        self.assertEqual(data.arguments, [])

        data = Routine('time_out', 'image', 'routine', 'arg0', 'arg1', 'arg2')
        self.assertEqual(data.time_out, 'time_out')
        self.assertEqual(data.image, 'image')
        self.assertEqual(data.routine, 'routine')
        self.assertListEqual(list(data.arguments), ['arg0', 'arg1', 'arg2'])

        # Procedure

        data = Procedure()
        self.assertEqual(data.time_out, None)
        self.assertEqual(data.language, None)
        self.assertEqual(data.procedure, None)
        self.assertEqual(data.arguments, [])

        data = Procedure('time_out', 'language', 'procedure', 'arg0', 'arg1', 'arg2')
        self.assertEqual(data.time_out, 'time_out')
        self.assertEqual(data.language, 'language')
        self.assertEqual(data.procedure, 'procedure')
        self.assertListEqual(list(data.arguments), ['arg0', 'arg1', 'arg2'])

        # Method

        data = Method()
        self.assertEqual(data.time_out, None)
        self.assertEqual(data.method, None)
        self.assertEqual(data.device, None)

        data = Method('time_out', 'method', 'device')
        self.assertEqual(data.time_out, 'time_out')
        self.assertEqual(data.method, 'method')
        self.assertEqual(data.device, 'device')

        # Dependency

        data = Dependency()
        self.assertEqual(data.treedep, 0)
        self.assertEqual(data.arguments, [])

        # TreeDEPENDENCY_AND = 10
        data = Dependency(10, 'first', 'second')
        self.assertEqual(data.treedep, 10)
        self.assertListEqual(list(data.arguments), ['first', 'second'])

        # Condition

        data = Condition()
        self.assertEqual(data.treecond, 0)
        self.assertEqual(data.condition, None)

        # TreeNEGATE_CONDITION = 7
        data = Condition(7, 'condition')
        self.assertEqual(data.treecond, 7)
        self.assertEqual(data.condition, 'condition')

        # WithUnits

        data = WithUnits()
        self.assertEqual(data.value, None)
        self.assertEqual(data.units, None)
        self.assertEqual(data.data(), None)

        data = WithUnits('value', 'units')
        self.assertEqual(data.value, 'value')
        self.assertEqual(data.units, 'units')
        self.assertEqual(data.data(), 'value')

        data = WithUnits(60.0, 'Hz')
        self.assertEqual(data.value, 60.0)
        self.assertEqual(data.units, 'Hz')
        self.assertEqual(data.data(), 60.0)

        data = WithUnits(Signal([1, 2, 3], None, [0.0, 0.1, 0.2]), 'counts')
        self.assertEqual(data.value, Signal([1, 2, 3], None, [0.0, 0.1, 0.2]))
        self.assertEqual(data.units, 'counts')
        self.assertEqual(data.data(), [1, 2, 3])

        # Call

        data = Call()
        self.assertEqual(data.return_dtype_id, DTYPE_L)
        self.assertEqual(data.image, None)
        self.assertEqual(data.routine, None)
        self.assertEqual(data.arguments, [])

        data = Call(DTYPE_MISSING, 'image', 'routine', 'arg0', 'arg1', 'arg2') # void
        self.assertEqual(data.return_dtype_id, DTYPE_MISSING)
        self.assertEqual(data.image, 'image')
        self.assertEqual(data.routine, 'routine')
        self.assertListEqual(list(data.arguments), ['arg0', 'arg1', 'arg2'])

        # WithError

        data = WithError()
        self.assertEqual(data.value, None)
        self.assertEqual(data.error, None)
        self.assertEqual(data.data(), None)
        self.assertEqual(data.getException(), None)

        data = WithError('value', 'error')
        self.assertEqual(data.value, 'value')
        self.assertEqual(data.error, 'error')
        self.assertEqual(data.data(), 'value')

        data = WithError(-1, '%TDI-E-INVCLADTY, Invalid mixture of storage class and data type')
        self.assertEqual(data.value, -1)
        self.assertEqual(data.error, '%TDI-E-INVCLADTY, Invalid mixture of storage class and data type')
        self.assertEqual(data.data(), -1)
        self.assertEqual(data.getException(), TdiINVCLADTY)

        # Opaque

        data = Opaque()
        self.assertEqual(data.value, None)
        self.assertEqual(data.opaque_type, None)
        self.assertEqual(data.data(), None)

        data = Opaque('value', 'opaque_type')
        self.assertEqual(data.value, 'value')
        self.assertEqual(data.opaque_type, 'opaque_type')
        self.assertEqual(data.data(), 'value')

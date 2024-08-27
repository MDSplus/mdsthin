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

from .exceptions import *
from .internals.dtypedef import *
from .internals.classdef import *
from .internals.mdsdescrip import *
from .internals.CvtConvertFloat import convert_float, convert_float_array

###
### Numeric
###

class Numeric:
    """
    Numeric type base class

    This contains the useful mathematical operators for all numeric types
    """

    def __new__(cls, *args, **kwargs):
        if cls is Numeric:
            raise Exception(f'Numeric cannot be instantiated directly')
        
        return object.__new__(cls)
    
    @property
    def __array_interface__(self):
        return self._data.__array_interface__
    
    def __int__(self):
        return int(self._data)
    
    def __float__(self):
        return float(self._data)
    
    def __add__(self, other):
        if isinstance(other, Signal):
            return Signal(self._data + other.data(), None, *other.dimensions)
        return Descriptor.from_data(self._data + other)
    
    def __sub__(self, other):
        if isinstance(other, Signal):
            return Signal(self._data - other.data(), None, *other.dimensions)
        return Descriptor.from_data(self._data - other)
    
    def __mul__(self, other):
        if isinstance(other, Signal):
            return Signal(self._data * other.data(), None, *other.dimensions)
        return Descriptor.from_data(self._data * other)
    
    def __pow__(self, other):
        if isinstance(other, Signal):
            return Signal(self._data ** other.data(), None, *other.dimensions)
        return Descriptor.from_data(self._data ** other)
    
    def __truediv__(self, other):
        if isinstance(other, Signal):
            return Signal(self._data / other.data(), None, *other.dimensions)
        return Descriptor.from_data(self._data / other)
    
    def __floordiv__(self, other):
        if isinstance(other, Signal):
            return Signal(self._data // other.data(), None, *other.dimensions)
        return Descriptor.from_data(self._data // other)
    
    def __mod__(self, other):
        if isinstance(other, Signal):
            return Signal(self._data % other.data(), None, *other.dimensions)
        return Descriptor.from_data(self._data % other)
    
    def __lshift__(self, other):
        return self.__class__(self._data << other)
    
    def __rshift__(self, other):
        return self.__class__(self._data >> other)
    
    def __and__(self, other):
        return self.__class__(self._data & other)
    
    def __or__(self, other):
        return self.__class__(self._data | other)
    
    def __xor__(self, other):
        return self.__class__(self._data ^ other)
    
    def __not__(self):
        return self.__class__(~self._data)
    
###
### Descriptor
###

class Descriptor:
    """
    Descriptor base class, which provides several useful methods for working with Descriptors.
    
    If called with no parameters, e.g. :class:`Descriptor()`, this will return the NULL Descriptor.
    
    If called with a python or numpy data type, it will coerce it into the proper MDSplus Descriptor
    subclass. e.g.:

    .. code-block:: python

        Descriptor(42) -> Int64(42)
        Descriptor(numpy.array([1, 2, 3], dtype=numpy.uint8)) -> UInt8Array([1, 2, 3])

    If you want to ensure that a given piece of data is a :class:`Descriptor`, call :meth:`Descriptor.from_data()`
    which will convert it if needed, or return the original :class:`Descriptor` if it already is one. e.g.

    .. code-block:: python

        Descriptor.from_data(42) -> Int64(42)
        Descriptor.from_data(Action(1, 2, 3)) -> Action(1, 2, 3)

    This also provides the :meth:`Descriptor.unpack()` and :meth:`Descriptor.pack()` methods, which are then
    overridden by each subclass as necessary. Also, the :meth:`Descriptor.serialize()` method will call
    :meth:`Descriptor.pack()`, but return the data as a `UInt8Array`. You could then call the
    :meth:`UInt8Array.deserialize()` method on either :class:`Int8Array` or :class:`UInt8Array` types.

    The `repr()` of a :class:`Descriptor` [sub]class should give you the TDI Decompile of that type. e.g.

    .. code-block:: python

        repr(Descriptor()) -> '*'
        repr(Int32(42)) -> '42L'
        repr(Signal([1, 2, 3], None, [4, 5, 6])) -> 'Build_Signal(Quadword([1, 2, 3]), *, Quadword([4, 5, 6]))'

    """

    def __new__(cls, data=None, dsc=None, *args, **kwargs):

        if cls is Descriptor:

            if dsc is not None:
                cls = DTYPE_CLASS_MAP[dsc.class_id][dsc.dtype_id]

            else:
                if isinstance(data, Descriptor):
                    cls = type(data)

                elif isinstance(data, str):
                    cls = String
                elif isinstance(data, bool):
                    cls = UInt8
                elif isinstance(data, int):
                    cls = Int64
                elif isinstance(data, float):
                    cls = Float64

                elif isinstance(data, (bytes, bytearray, memoryview)):
                    cls = UInt8Array
                elif isinstance(data, list):
                    cls = List
                elif isinstance(data, tuple):
                    cls = Tuple
                elif isinstance(data, dict):
                    cls = Dictionary

                elif isinstance(data, numpy.number):
                    
                    for dtype_id, numpy_dtype in NUMPY_DTYPE_MAP.items():
                        if data.dtype == numpy_dtype:
                            cls = DTYPE_CLASS_MAP[CLASS_S][dtype_id]
                            break

                elif isinstance(data, numpy.ndarray):
                    
                    for dtype_id, numpy_dtype in NUMPY_DTYPE_MAP.items():
                        if data.dtype == numpy_dtype:
                            cls = DTYPE_CLASS_MAP[CLASS_A][dtype_id]
                            break

                    if data.dtype.char in ['U', 'S']:
                        cls = StringArray
        
        if cls is Descriptor:
            return object.__new__(cls)
        
        return cls.__new__(cls)

    def __init__(self, data=None, dsc=None):
        self._dsc = dsc
        self._data = data

        if self._dsc is None:
            self._dsc = mdsdsc_t(
                length=0,
                class_id=CLASS_MISSING,
                dtype_id=DTYPE_MISSING,
                offset=0
            )

    @property
    def length(self):
        """
        :class:`mdsdsc_t`.length
        """

        return self._dsc.length
    
    @property
    def dtype_id(self):
        """
        :class:`mdsdsc_t`.dtype_id
        """

        return self._dsc.dtype_id

    @property
    def dtype_str(self):
        """
        dtype_to_string(:class:`mdsdsc_t`.dtype_id)
        """

        return dtype_to_string(self._dsc.dtype_id)
    
    @property
    def class_id(self):
        """
        :class:`mdsdsc_t`.class_id
        """

        return self._dsc.class_id
    
    @property
    def class_str(self):
        """
        class_to_string(:class:`mdsdsc_t`.class_id)
        """

        return class_to_string(self._dsc.class_id)

    @property
    def offset(self):
        """
        :class:`mdsdsc_t`.offset
        """

        return self._dsc.offset

    def data(self):
        """
        Get the data for this descriptor

        :return: Return the data in this descriptor as a python/numpy type.
        :rtype: The python/numpy type of the underlying data, overridden by all subclasses.
        """

        return self._data
    
    def decompile(self):
        """
        Return the decompiled TDI representation of the data.
        """

        return repr(self)

    def __repr__(self):
        if self._data is None:
            return '*'
        return f'{self.__class__.__name__}({self._data})'
    
    def __eq__(self, other):
        if isinstance(other, Descriptor):
            other = other.data()
        return self.data() == other
    
    def __hash__(self):
        return hash(self.data())
    
    def serialize(self):
        return UInt8Array(self.pack())
    
    @staticmethod
    def from_data(data):
        """
        Ensure that the given data is a :class:`Descriptor` type. If the data is already
        a :class:`Descriptor`, then just return it. Otherwise, call :class:`Descriptor(data)`

        :param data: The data to possibly convert into a :class:`Descriptor`
        :type data: python/numpy type or :class:`Descriptor`
        :return: The data as a :class:`Descriptor`
        :rtype: Descriptor
        """

        if isinstance(data, Descriptor):
            return data
        
        return Descriptor(data)
    
    def pack(self):
        """
        Pack the :class:`Descriptor` into a serialized array of bytes, starting with the `mdsdsc_t` header.
        This is overridden by all subclasses.

        :return: The :class:`Descriptor` serialized into bytes.
        :rtype: `bytearray()`
        """
        return bytearray()
    
    @staticmethod
    def unpack(buffer, conn=None):
        """
        Unpack the given buffer and construct the corresponding :class:`Descriptor` subclass. This requires a
        buffer with a `mdsdsc_t` header.

        :param buffer: The buffer to unpack.
        :type buffer: bytes, bytearray or any type that implements the buffer protocol.
        :param Connection conn: The connection, used to gather missing metadata, such as the FULLPATH
            of a given NID, defaults to None
        :return: An instance of a :class:`Descriptor` subclass containing the data.
        :rtype: A subclass of :class:`Descriptor`
        :raises MdsException: if there are problems unpacking the data.
        """

        buffer = bytearray(buffer)
        
        # TODO: Improve?
        dtype_id = buffer[2]
        class_id = buffer[3]

        if class_id not in DTYPE_CLASS_MAP:
            raise MdsException('Invalid class:', class_to_string(class_id))
        
        if dtype_id not in DTYPE_CLASS_MAP[class_id]:
            raise MdsException('Invalid dtype for class:', dtype_to_string(dtype_id), class_to_string(class_id))

        dtype_class = DTYPE_CLASS_MAP[class_id][dtype_id]

        if issubclass(dtype_class, DescriptorS):

            dsc = mdsdsc_s_t.from_buffer(buffer)

            if dsc.length == 0:
                dsc.length = get_dtype_size(dsc.dtype_id)

            if dsc.offset == 0:
                dsc.offset = ctypes.sizeof(dsc)

            data = None
            data_buffer = buffer[ dsc.offset : dsc.offset + dsc.length ]
            
            if dsc.dtype_id in NUMPY_DTYPE_MAP:
                data = numpy.frombuffer(data_buffer, dtype=NUMPY_DTYPE_MAP[dtype_id], count=1)[0]
            
            elif dsc.dtype_id == DTYPE_T:
                data = data_buffer.decode('ascii')
            
            elif dsc.dtype_id in [ DTYPE_F, DTYPE_D, DTYPE_G ]:
                data = convert_float(dsc.dtype_id, data_buffer)

            if dtype_class is TreeNID:
                return TreeNID(data, conn=conn)
                
            return dtype_class(data)

        elif issubclass(dtype_class, DescriptorA):

            dsc = mdsdsc_a_t.from_buffer(buffer)

            if dsc.length == 0:
                dsc.length = get_dtype_size(dsc.dtype_id)

            count = dsc.arsize // dsc.length
            shape = (count,)
            order = 'C' # C-style Row-Major

            if dsc.scale > 0:
                raise MdsException('Array scale unimplemented')
            
            if dsc.digits > 0:
                raise MdsException('Array digits unimplemented')
            
            if dsc.aflags.binscale:
                raise MdsException('Array binscale unimplemented')
            
            # if dsc.aflags.redim:
            #     raise MdsException('Array redim unimplemented')

            if dsc.aflags.coeff:

                a0_coeff_buffer = buffer[ ctypes.sizeof(dsc) : ]
                a0_coeff = numpy.frombuffer(a0_coeff_buffer, dtype='uint32', count=(1 + dsc.dimct))
                
                a0 = a0_coeff[0]
                coeff = a0_coeff[1 : ]

                dsc.offset = a0 # "address of element whos index is all zeros"
                shape = coeff[ : : -1]

                if dsc.aflags.bounds:
                    raise MdsException('Array bounds unimplemented')
            
            # The inverse from what the documentation claims...
            if not dsc.aflags.column:
                order = 'F' # Fortran-style Column-Major

            data = None
            data_buffer = buffer[ dsc.offset : dsc.offset + dsc.arsize ]
            
            if dtype_id in NUMPY_DTYPE_MAP:
                data = numpy.frombuffer(data_buffer, dtype=NUMPY_DTYPE_MAP[dtype_id], count=count)
            
            elif dtype_id == DTYPE_T:
                data = numpy.frombuffer(data_buffer, dtype=f'|S{dsc.length}').astype(str)

            elif dsc.dtype_id in [ DTYPE_F, DTYPE_D, DTYPE_G ]:
                data = convert_float_array(dsc.dtype_id, data_buffer)

            data = data.reshape(shape, order=order)
                
            return dtype_class(data)
        
        elif issubclass(dtype_class, DescriptorAPD):

            dsc = mdsdsc_a_t.from_buffer(buffer)

            if dsc.offset == 0:
                dsc.offset = ctypes.sizeof(dsc)

            if dsc.length != 4:
                raise MdsException('APD length != 4')

            offsets_buffer = buffer[ dsc.offset : dsc.offset + dsc.arsize ]
            offsets = numpy.frombuffer(offsets_buffer, dtype=numpy.uint32)

            descs = []
            for offset in offsets:
                if offset == 0:
                    descs.append(Descriptor())
                    continue

                data_buffer = buffer[offset : ]
                descs.append(Descriptor.unpack(data_buffer, conn=conn))

            return dtype_class(descs=descs)
            
        elif issubclass(dtype_class, DescriptorR):

            dsc = mdsdsc_r_t.from_buffer(buffer)

            offsets_buffer = buffer[ ctypes.sizeof(dsc) : ]
            offsets = numpy.frombuffer(offsets_buffer, dtype=numpy.uint32, count=dsc.ndesc)

            arguments = []

            data_buffer = buffer[ dsc.offset : ]
            if dsc.length == 1:
                arguments.append(Int8(numpy.frombuffer(data_buffer, dtype=numpy.uint8, count=1)[0]))
            elif dsc.length == 2:
                arguments.append(Int16(numpy.frombuffer(data_buffer, dtype=numpy.uint16, count=1)[0]))

            for i in range(dsc.ndesc):
                if offsets[i] == 0:
                    arguments.append(Descriptor())
                    continue

                dscptr_buffer = buffer[ offsets[i] : ]
                arguments.append(Descriptor.unpack(dscptr_buffer, conn=conn))

            return dtype_class(*arguments)

###
### DescriptorS
###

class DescriptorS(Descriptor):
    """
    A subclass of :class:`Descriptor` representing CLASS_S types.
    """

    def __new__(cls, *args, **kwargs):
        if cls is DescriptorS:
            raise Exception(f'DescriptorS cannot be instantiated directly')
        
        return object.__new__(cls)

    def __init__(self, data, dsc):
        
        dsc.class_id = CLASS_S
        dsc.offset = ctypes.sizeof(dsc)

        super().__init__(data=data, dsc=dsc)
    
    def pack(self):
        return self.pack_header() + self.pack_data()
    
    def pack_header(self):
        """
        Pack just the `mdsdsc_s_t` header into a bytearray.

        :return: The serialized bytes of the `mdsdsc_s_t`.
        :rtype: `bytearray`
        """

        return bytearray(self._dsc)
        
    def pack_data(self):
        """
        Pack just the data into a bytearray.

        :return: The serialized data.
        :rtype: `bytearray`
        """

        return bytearray(self._data.tobytes())
    
    @staticmethod
    def unpack_data(dtype_id, buffer, length=0):
        """
        Unpack just the data, along with a given `dtype_id` in lieu of a full `mdsdsc_s_t.
        This is overridden by some subclasses.

        :param int dtype_id: The `DTYPE_{type}` enum corresponding to the data type.
        :return: An instance of a :class:`DescriptorS` subclass containing the data.
        :rtype: A subclass of :class:`DescriptorS`
        """

        dtype_class = DTYPE_CLASS_MAP[CLASS_S][dtype_id]

        if dtype_id in NUMPY_DTYPE_MAP:
            numpy_dtype = NUMPY_DTYPE_MAP[dtype_id]
            data = numpy.frombuffer(buffer, dtype=numpy_dtype, count=1)[0]

        elif dtype_id == DTYPE_T:
            if length > 0:
                data = buffer[ : length ].decode('ascii')
            else:
                data = buffer.decode('ascii')

        return dtype_class(data)

class String(DescriptorS):

    def __init__(self, data=''):
        data = str(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=len(data.encode('ascii')),
                dtype_id=DTYPE_T,
            ),
        )

    def __repr__(self):
        return f'"{self._data}"'

    def pack_data(self):
        return bytearray(self._data.encode('ascii'))
    
    @staticmethod
    def unpack_data(buffer, length=0):
        if length > 0:
            return String(buffer[ : length ].decode('ascii'))
        
        return String(buffer.decode('ascii'))

class Ident(DescriptorS):
    def __init__(self, data=''):
        data = str(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=len(data.encode('ascii')),
                dtype_id=DTYPE_IDENT,
            ),
        )

    def __repr__(self):
        return str(self._data)

    def pack_data(self):
        return bytearray(self._data.encode('ascii'))
    
    @staticmethod
    def unpack_data(buffer, length=0):
        if length > 0:
            return Ident(buffer[ : length ].decode('ascii'))
        
        return Ident(buffer.decode('ascii'))

class TreeNID(DescriptorS):
    def __init__(self, data=0, conn=None):
        if isinstance(data, Descriptor):
            data = data.data()

        data = numpy.uint32(data)
        self._conn = conn

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_NID,
            ),
        )

    def __repr__(self):
        if self._conn is not None:
            return self._conn.get(f'getnci({self._data}, "FULLPATH")').data()
        
        return f'NID({self._data})'

class TreePath(DescriptorS):
    def __init__(self, data=''):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = str(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=len(data.encode('ascii')),
                dtype_id=DTYPE_T,
            ),
        )

    def __repr__(self):
        return str(self._data)

    def pack_data(self):
        return bytearray(self._data.encode('ascii'))
    
    @staticmethod
    def unpack_data(buffer, length=0):
        if length > 0:
            return TreePath(buffer[ : length ].decode('ascii'))
    
        return TreePath(buffer.decode('ascii'))

class UInt8(DescriptorS, Numeric):
    def __init__(self, data=0):
        if isinstance(data, Descriptor):
            data = data.data()

        data = numpy.uint8(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_BU,
            ),
        )

    def __repr__(self):
        return f'{self.data()}BU'
    
class UInt16(DescriptorS, Numeric):
    def __init__(self, data=0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.uint16(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_WU,
            ),
        )

    def __repr__(self):
        return f'{self.data()}WU'

class UInt32(DescriptorS, Numeric):
    def __init__(self, data=0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.uint32(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_LU,
            ),
        )

    def __repr__(self):
        return f'{self.data()}LU'

class UInt64(DescriptorS, Numeric):
    def __init__(self, data=0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.uint64(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_QU,
            ),
        )

    def __repr__(self):
        return f'{self.data()}QU'

class Int8(DescriptorS, Numeric):
    def __init__(self, data=0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.int8(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_B,
            ),
        )

    def __repr__(self):
        return f'{self.data()}B'

class Int16(DescriptorS, Numeric):
    def __init__(self, data=0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.int16(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_W,
            ),
        )

    def __repr__(self):
        return f'{self.data()}W'

class Int32(DescriptorS, Numeric):
    def __init__(self, data=0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.int32(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_L,
            ),
        )

    def __repr__(self):
        return f'{self.data()}L'

class Int64(DescriptorS, Numeric):
    def __init__(self, data=0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.int64(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_Q,
            ),
        )

    def __repr__(self):
        return f'{self.data()}Q'

class Float32(DescriptorS, Numeric):
    def __init__(self, data=0.0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.float32(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_FS,
            ),
        )

    def __repr__(self):
        return f'{self.data()}F0'

class Float64(DescriptorS, Numeric):
    def __init__(self, data=0.0):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.float64(data)

        super().__init__(
            data=data,
            dsc=mdsdsc_s_t(
                length=data.itemsize,
                dtype_id=DTYPE_FT,
            ),
        )

    def __repr__(self):
        return f'{self.data()}D0'

###
### DescriptorA
###

class DescriptorA(Descriptor):

    def __new__(cls, *args, **kwargs):
        if cls is DescriptorA:
            raise Exception(f'DescriptorA cannot be instantiated directly')
        
        return object.__new__(cls)

    def __init__(self, data, dsc, dims=[]):
        
        self._dims = tuple(dims)

        if isinstance(data, numpy.ndarray): # TODO: StringArray
            self._dims = data.shape[::-1]
            dsc.length = data.itemsize
            dsc.arsize = data.size * data.itemsize

        dsc.offset = ctypes.sizeof(dsc)
        dsc.dimct = len(self._dims)
        dsc.aflags.redim = 1 # Indicate that this array can be redimensioned
        dsc.aflags.column = 1 # Opposite to what the comments claim, this indicates row-major
        dsc.aflags.coeff = (dsc.dimct > 1)

        if dsc.aflags.coeff:
            # a0
            dsc.offset += ctypes.sizeof(ctypes.c_uint32)

            # coeff
            dsc.offset += ctypes.sizeof(ctypes.c_uint32) * dsc.dimct

        super().__init__(data=data, dsc=dsc)

    def __eq__(self, other):
        if isinstance(other, Descriptor):
            other = other.data()

        # numpy.array(bool).all()
        return (self.data() == other).all()

    def __ne__(self, other):
        if isinstance(other, Descriptor):
            other = other.data()

        # numpy.array(bool).any()
        return (self.data() != other).any()
    
    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, index):
        return self._data[index]
    
    @property
    def scale(self):
        """mdsdsc_a_t.scale"""
        return self._dsc.scale

    @property
    def digits(self):
        """mdsdsc_a_t.digits"""
        return self._dsc.digits

    @property
    def aflags(self):
        """mdsdsc_a_t.aflags"""
        return self._dsc.aflags
    
    @property
    def dimct(self):
        """mdsdsc_a_t.dimct"""
        return self._dsc.dimct
    
    @property
    def dims(self):
        """mdsdsc_a_t.dims"""
        return self._dims
    
    @property
    def arsize(self):
        """mdsdsc_a_t.arsize"""
        return self._dsc.arsize
    
    def pack(self):
        return self.pack_header() + self.pack_data()
    
    def pack_header(self):
        buffer = bytearray(self._dsc)

        if self._dsc.aflags.coeff:
            a0_coeffs = [self._dsc.offset] + list(self._dims)
            a0_coeffs = numpy.array(a0_coeffs, dtype=numpy.int32)
            buffer += a0_coeffs.tobytes()

        return buffer
        
    def pack_data(self):
        return bytearray(self._data.tobytes())
    
    @staticmethod
    def unpack_data(dtype_id, buffer, dims=[], length=0):
        dtype_class = DTYPE_CLASS_MAP[CLASS_A][dtype_id]

        if dtype_id in NUMPY_DTYPE_MAP:
            numpy_dtype = NUMPY_DTYPE_MAP[dtype_id]
            data = numpy.frombuffer(buffer, dtype=numpy_dtype)

        elif dtype_id == DTYPE_T:
            data = numpy.frombuffer(buffer, dtype=f'|S{length}').astype(str)

        else:
            raise MdsException(f'Unable to unpack array data with {dtype_to_string(dtype_id)}')
        
        if len(dims) > 0:
            data = data.reshape(dims[::-1])

        return dtype_class(data)

class StringArray(DescriptorA):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()

        data = numpy.array(data, dtype=str)
        shape = data.shape

        # Iterating over a flat array is considerably easier than using numpy.nditer
        data = data.flatten()

        # Ensure that all elements are the same size by padding them with trailing spaces
        maxlen = data.itemsize
        for i, s in enumerate(data):
            data[i] = s.ljust(maxlen)

        # Put our original shape back
        data = data.reshape(shape)
        
        # Force numpy to use ASCII (well, UTF-8) instead of UTF-32
        data = data.astype(bytes)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_T,
            ),
        )

    def __repr__(self):
        return repr(self._data.astype(str).tolist())

    def __eq__(self, other):
        if isinstance(other, Descriptor):
            other = other.data()

        # numpy.array(bool).all()
        return (self.data().astype(str) == other.astype(str)).all()

    def __ne__(self, other):
        if isinstance(other, Descriptor):
            other = other.data()

        # numpy.array(bool).any()
        return (self.data().astype(str) != other.astype(str)).any()

    def __iter__(self):
        return self.data().__iter__()

    def __getitem__(self, index):
        return self.data()[index]
    
    def data(self):
        tmp = self._data.astype(str).flatten()

        for i, s in enumerate(tmp):
            tmp[i] = s.rstrip()

        return tmp.reshape(self._data.shape)
    
    def data_raw(self):
        return self._data.astype(str)

class UInt8Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()

        elif isinstance(data, (bytes, bytearray, memoryview)):
            data = numpy.frombuffer(data, dtype=numpy.uint8)

        else:
            data = numpy.array(data, dtype=numpy.uint8)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_BU,
            ),
        )

    def __repr__(self):
        return f'Byte_Unsigned({repr(self._data.tolist())})'

    def deserialize(self, conn=None):
        return Descriptor.unpack(bytearray(self.data().tobytes()), conn=conn)

class UInt16Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()

        data = numpy.array(data, dtype=numpy.uint16)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_WU,
            ),
        )

    def __repr__(self):
        return f'Word_Unsigned({repr(self._data.tolist())})'

class UInt32Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.array(data, dtype=numpy.uint32)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_LU,
            ),
        )

    def __repr__(self):
        return f'Long_Unsigned({repr(self._data.tolist())})'

class UInt64Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.array(data, dtype=numpy.uint64)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_QU,
            ),
        )

    def __repr__(self):
        return f'Quadword_Unsigned({repr(self._data.tolist())})'

class Int8Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()
            
        elif isinstance(data, (bytes, bytearray, memoryview)):
            data = numpy.frombuffer(data, dtype=numpy.int8)

        else:
            data = numpy.array(data, dtype=numpy.int8)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_B,
            ),
        )

    def __repr__(self):
        return f'Byte({repr(self._data.tolist())})'

    def deserialize(self, conn=None):
        return Descriptor.unpack(bytearray(self.data().tobytes()), conn=conn)

class Int16Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.array(data, dtype=numpy.int16)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_W,
            ),
        )

    def __repr__(self):
        return f'Word({repr(self._data.tolist())})'

class Int32Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.array(data, dtype=numpy.int32)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_L,
            ),
        )

    def __repr__(self):
        return f'Long({repr(self._data.tolist())})'

class Int64Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.array(data, dtype=numpy.int64)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_Q,
            ),
        )

    def __repr__(self):
        return f'Quadword({repr(self._data.tolist())})'

class Float32Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.array(data, dtype=numpy.float32)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_FS,
            ),
        )

    def __repr__(self):
        return f'FS_FLOAT({repr(self._data.tolist())})'

class Float64Array(DescriptorA, Numeric):
    def __init__(self, data=[]):
        if isinstance(data, Descriptor):
            data = data.data()
            
        data = numpy.array(data, dtype=numpy.float64)

        super().__init__(
            data=data,
            dsc=mdsdsc_a_t(
                class_id=CLASS_A,
                dtype_id=DTYPE_FT,
            ),
        )

    def __repr__(self):
        return f'FT_FLOAT({repr(self._data.tolist())})'
    
###
### DescriptorAPD
###

class DescriptorAPD(Descriptor):

    def __new__(cls, *args, **kwargs):
        if cls is DescriptorAPD:
            raise Exception(f'DescriptorAPD cannot be instantiated directly')
        
        return object.__new__(cls)

    def __init__(self, data, count, dsc):

        # TODO:
        
        dsc.class_id = CLASS_APD
        dsc.length = ctypes.sizeof(ctypes.c_uint32)
        dsc.arsize = count * dsc.length
        dsc.dimct = 1

        super().__init__(data=data, dsc=dsc)

    def data(self):
        return self

    @property
    def scale(self):
        """mdsdsc_a_t.scale"""
        return self._dsc.scale

    @property
    def digits(self):
        """mdsdsc_a_t.digits"""
        return self._dsc.digits

    @property
    def aflags(self):
        """mdsdsc_a_t.aflags"""
        return self._dsc.aflags
    
    @property
    def dimct(self):
        """mdsdsc_a_t.dimct"""
        return self._dsc.dimct
    
    @property
    def dims(self):
        """mdsdsc_a_t.1]"""
        return self._data.shape[::-1]
    
    @property
    def arsize(self):
        """mdsdsc_a_t.arsize"""
        return self._dsc.arsize
    
    @property
    def descs(self):
        return list(self)

    def __repr__(self):
        return f'{self.__class__.__name__}({",".join(map(repr, self.descs))})'
    
    def pack(self):

        count = self._dsc.arsize // self._dsc.length
        offsets = numpy.zeros(count, dtype=numpy.uint32)

        data_buffer = bytearray()
        data_offset = ctypes.sizeof(self._dsc) + (offsets.itemsize * offsets.size)

        for i, value in enumerate(self.descs):

            if type(value) is Descriptor:
                offsets[i] = 0
                continue

            offsets[i] = data_offset + len(data_buffer)
            data_buffer += value.pack()

        return bytearray(bytes(self._dsc) + offsets.tobytes() + data_buffer)
    
class List(DescriptorAPD):
    
    def __init__(self, *items, descs=[]):

        data = []

        if len(items) == 1 and isinstance(items[0], Descriptor):
            items = items[0].data()

        # If this has been called as List(list)
        if len(items) == 1 and isinstance(items[0], (list, tuple)):
            for item in items[0]:
                data.append(Descriptor.from_data(item))

        else:
            for item in items:
                data.append(Descriptor.from_data(item))

        data.extend(descs)

        super().__init__(
            data=data,
            count=len(data),
            dsc=mdsdsc_a_t(
                dtype_id=DTYPE_LIST,
            )
        )

    def __repr__(self):
        if len(self._data) == 0:
            return 'List()'
        return f'List(,{",".join(map(repr, self._data))})'

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, index):
        return self._data[index]
    
    def __setitem__(self, index, value):
        self._data[index] = Descriptor.from_data(value)
        self._dsc.arsize = len(self._data) * self._dsc.length
    
    def append(self, value):
        self._data.append(Descriptor.from_data(value))
        self._dsc.arsize = len(self._data) * self._dsc.length

    def remove(self, value):
        self._data.remove(Descriptor.from_data(value))
        self._dsc.arsize = len(self._data) * self._dsc.length

    def data(self):
        return self._data

# Trying to subclass tuple causes issues
class Tuple(DescriptorAPD):
    
    def __init__(self, *items, descs=[]):

        data = []

        if len(items) == 1 and isinstance(items[0], Descriptor):
            items = items[0].data()
            
        # If this has been called as Tuple(tuple)
        if len(items) == 1 and isinstance(items[0], (list, tuple)):
            for item in items[0]:
                data.append(Descriptor.from_data(item))

        else:
            for item in items:
                data.append(Descriptor.from_data(item))

        data.extend(descs)

        super().__init__(
            data=tuple(data),
            count=len(data),
            dsc=mdsdsc_a_t(
                dtype_id=DTYPE_TUPLE,
            )
        )

    def __repr__(self):
        if len(self._data) == 0:
            return 'Tuple()'
        return f'Tuple(,{",".join(map(repr, self._data))})'

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, index):
        return self._data[index]

    def data(self):
        return tuple(self._data)

class Dictionary(DescriptorAPD):
    
    # dict or key, value, ...repeat
    def __init__(self, *pairs, descs=[]):

        if len(pairs) == 1 and isinstance(pairs[0], Descriptor):
            pairs = pairs[0].data()

        # If this has been called as Dictionary(dict)
        if len(pairs) == 1 and isinstance(pairs[0], dict):
            pairs = list(pairs[0].items())

        # If the entire list contains key/value tuples
        elif all([ (isinstance(pair, tuple) and len(pair) == 2) for pair in pairs ]):
            pairs = list(pairs)
            
        else:
            from itertools import islice, izip
            pairs = izip(islice(pairs, None, None, 2), islice(pairs, 1, None, 2))

        data = {}
        for k, v in pairs:
            data[Descriptor.from_data(k)] = Descriptor.from_data(v)

        if (len(descs) % 2) != 0:
            raise Exception('Cannot create Dictionary, descs must be a list of key/value pairs')

        for i in range(0, len(descs), 2):
            data[descs[i]] = descs[i + 1]

        super().__init__(
            data=data,
            count=len(data) * 2,
            dsc=mdsdsc_a_t(
                dtype_id=DTYPE_DICTIONARY,
            )
        )

    def __repr__(self):
        return f'Dictionary({", ".join(list(map(repr, self.items())))})'

    def __repr__(self):
        if len(self._data) == 0:
            return 'Dict()'
        return f'Dict(,{",".join([ f" {repr(k)},{repr(v)}" for k,v in self._data.items() ])})'
    
    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()
    
    def __contains__(self, key):
        return self._data.__contains__(key)
    
    def __getitem__(self, key):
        return self._data.__getitem__(key)
    
    def __setitem__(self, key, value):
        self._data[Descriptor.from_data(key)] = Descriptor.from_data(value)
        self._dsc.arsize = (len(self._data) * 2) * self._dsc.length
    
    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()
    
    def items(self):
        return self._data.items()
    
    def get(self, key, default):
        return self._data.get(key, default)

    def data(self):
        return dict(self._data)
    
    @property
    def descs(self):
        descs = []
        for k, v in self.items():
            descs.append(k)
            descs.append(v)
        return descs

###
### DescriptorR
###

# TODO: data = Signal(); data2 = Signal(data)

class DescriptorR(Descriptor):

    def __new__(cls, *args, **kwargs):
        if cls is DescriptorR:
            raise Exception(f'DescriptorR cannot be instantiated directly')
        
        return object.__new__(cls)
    
    def __init__(self, dsc, dscptrs, data=None):
        
        dsc.class_id = CLASS_R
        dsc.ndesc = len(dscptrs)
        
        self._dscptrs = [ Descriptor.from_data(dscptr) for dscptr in dscptrs ]

        if data is not None:
            dsc.length = data.itemsize

        super().__init__(data=data, dsc=dsc)

    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(map(repr, self._dscptrs))})'
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        
        if self._data != other._data:
            return False
        
        if len(self._dscptrs) != len(other._dscptrs):
            return False
        
        for ours, theirs in zip(self._dscptrs, other._dscptrs):
            if ours != theirs:
                return False

        return True
    
    @property
    def ndesc(self):
        """mdsdsc_r_t.ndesc"""
        return self._dsc.ndesc
    
    @property
    def dscptrs(self):
        """mdsdsc_r_t.dscptrs"""
        return self._dscptrs

    def data(self):
        return self
    
    def pack(self):
        offsets = numpy.zeros(self._dsc.ndesc, dtype=numpy.uint32)

        dscptrs_buffer = bytearray()
        dscptrs_offset = ctypes.sizeof(self._dsc) + (offsets.itemsize * offsets.size)

        data_buffer = bytearray()
        if self._data is not None:
            self._dsc.length = self._data.itemsize
            self._dsc.offset = dscptrs_offset
            dscptrs_offset += self._data.itemsize
            data_buffer = bytearray(self._data.tobytes())

        for i, dscptr in enumerate(self.dscptrs):

            if type(dscptr) is Descriptor:
                offsets[i] = 0
                continue

            offsets[i] = dscptrs_offset + len(dscptrs_buffer)
            dscptrs_buffer += dscptr.pack()

        return bytearray(bytes(self._dsc) + offsets.tobytes() + data_buffer + dscptrs_buffer)

class Signal(DescriptorR):
    
    def __init__(self, value=None, raw=None, *dimensions):
        super().__init__(
            dscptrs=[value, raw, *dimensions],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_SIGNAL,
            )
        )

    @property
    def value(self):
        return self._dscptrs[0]
    
    @property
    def raw(self):
        return self._dscptrs[1]
    
    @property
    def dimensions(self):
        return self._dscptrs[2 : ]

    def __repr__(self):
        return f'Build_Signal({", ".join(map(repr, self._dscptrs))})'

    def data(self):
        if type(self.value) is not Descriptor:
            return self.value.data()
        return self.raw.data()
    
    def raw_of(self):
        return self._dscptrs[1]

    def dim_of(self, index=0):
        return self.dimensions[index]

class Dimension(DescriptorR):
    
    def __init__(self, window=None, axis=None):
        super().__init__(
            dscptrs=[window, axis],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_DIMENSION,
            )
        )

    @property
    def window(self):
        return self._dscptrs[0]
    
    @property
    def axis(self):
        return self._dscptrs[1]

    def __repr__(self):
        return f'Build_Dimension({", ".join(map(repr, self._dscptrs))})'

class Window(DescriptorR):
    
    def __init__(self, startidx=None, endingidx=None, value_at_idx0=None):
        super().__init__(
            dscptrs=[startidx, endingidx, value_at_idx0],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_WINDOW,
            )
        )

    @property
    def startidx(self):
        return self._dscptrs[0]

    @property
    def endingidx(self):
        return self._dscptrs[1]

    @property
    def value_at_idx0(self):
        return self._dscptrs[2]

    def __repr__(self):
        return f'Build_Window({", ".join(map(repr, self._dscptrs))})'

class Slope(DescriptorR):
    
    # slope, begin, ending, ...repeat
    def __init__(self, *segments):
        if (len(segments) % 3) != 0:
            raise Exception('len(segments) must be a multiple of 3')
        
        super().__init__(
            dscptrs=[*segments],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_SLOPE,
            )
        )

    @property
    def segments(self):
        segments = []
        for i in range(0, len(self._dscptrs), 3):
            segments.append((self._dscptrs[i], self._dscptrs[i + 1], self._dscptrs[i + 2]))
        return segments

    def __repr__(self):
        return f'Build_Slope({", ".join(map(repr, self._dscptrs))})'

class Function(DescriptorR):
    
    def __init__(self, opcode=0, *arguments):

        # e.g. 'ADD' -> 38
        if isinstance(opcode, str):
            from .internals.opcbuiltins import OPCODE_MAP
            opcode = OPCODE_MAP.get(opcode.upper(), -1)

        super().__init__(
            data=numpy.uint16(opcode),
            dscptrs=[*arguments],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_FUNCTION,
            )
        )

    @property
    def opcode(self):
        return self._data

    @property
    def arguments(self):
        return self._dscptrs

    def __repr__(self):
        from .internals.opcbuiltins import OPCODE_REPR_MAP
        if self._data in OPCODE_REPR_MAP:
            return OPCODE_REPR_MAP[self._data](*self._dscptrs)
        return f'Build_Function({self._data}, {", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        raise Exception('Evaluating functions is not implemented')

class Conglom(DescriptorR):
    
    def __init__(self, image=None, model=None, name=None, qualifiers=None):
        super().__init__(
            dscptrs=[image, model, name, qualifiers],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_CONGLOM,
            )
        )

    @property
    def image(self):
        return self._dscptrs[0]

    @property
    def model(self):
        return self._dscptrs[1]

    @property
    def name(self):
        return self._dscptrs[2]

    @property
    def qualifiers(self):
        return self._dscptrs[3]

    def __repr__(self):
        return f'Build_Conglom({", ".join(map(repr, self._dscptrs))})'

class Range(DescriptorR):
    
    def __init__(self, begin=None, ending=None, deltaval=None):
        super().__init__(
            dscptrs=[begin, ending, deltaval],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_RANGE,
            )
        )

    @property
    def begin(self):
        return self._dscptrs[0]

    @property
    def ending(self):
        return self._dscptrs[1]

    @property
    def deltaval(self):
        return self._dscptrs[2]

    def __repr__(self):
        return f'Build_Range({", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        return range(self.begin.data(), self.ending.data(), self.deltaval.data())
    
    # TODO: iterator?
    
class Action(DescriptorR):

    def __init__(self, dispatch=None, task=None, errorlogs=None, completion_message=None, performance=None):
        super().__init__(
            dscptrs=[dispatch, task, errorlogs, completion_message, performance],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_ACTION,
            )
        )
    
    @property
    def dispatch(self):
        return self._dscptrs[0]
    
    @property
    def task(self):
        return self._dscptrs[1]
    
    @property
    def errorlogs(self):
        return self._dscptrs[2]
    
    @property
    def completion_message(self):
        return self._dscptrs[3]
    
    @property
    def performance(self):
        return self._dscptrs[4]

    def __repr__(self):
        return f'Build_Action({", ".join(map(repr, self._dscptrs))})'

class Dispatch(DescriptorR):
    
    def __init__(self, treesched=0, ident=None, phase=None, when=None, completion=None):
        super().__init__(
            data=numpy.uint8(treesched),
            dscptrs=[ident, phase, when, completion],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_DISPATCH,
            )
        )

    @property
    def treesched(self):
        return self._data

    @property
    def ident(self):
        return self._dscptrs[0]

    @property
    def phase(self):
        return self._dscptrs[1]

    @property
    def when(self):
        return self._dscptrs[2]

    @property
    def completion(self):
        return self._dscptrs[3]

    def __repr__(self):
        return f'Build_Dispatch({self._data}, {", ".join(map(repr, self._dscptrs))})'

class Program(DescriptorR):
    
    def __init__(self, time_out=None, program=None):
        super().__init__(
            dscptrs=[time_out, program],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_PROGRAM,
            )
        )

    @property
    def time_out(self):
        return self._dscptrs[0]

    @property
    def program(self):
        return self._dscptrs[1]

    def __repr__(self):
        return f'Build_Program({", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        raise Exception('Programs are not implemented')

class Routine(DescriptorR):
    
    def __init__(self, time_out=None, image=None, routine=None, *arguments):
        super().__init__(
            dscptrs=[time_out, image, routine, *arguments],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_ROUTINE,
            )
        )

    @property
    def time_out(self):
        return self._dscptrs[0]

    @property
    def image(self):
        return self._dscptrs[1]

    @property
    def routine(self):
        return self._dscptrs[2]

    @property
    def arguments(self):
        return self._dscptrs[3 : ]

    def __repr__(self):
        return f'Build_Routine({", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        raise Exception('Routines are not implemented')

class Procedure(DescriptorR):
    
    def __init__(self, time_out=None, language=None, procedure=None, *arguments):
        super().__init__(
            dscptrs=[time_out, language, procedure, *arguments],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_PROCEDURE,
            )
        )

    @property
    def time_out(self):
        return self._dscptrs[0]

    @property
    def language(self):
        return self._dscptrs[1]

    @property
    def procedure(self):
        return self._dscptrs[2]

    @property
    def arguments(self):
        return self._dscptrs[3 : ]

    def __repr__(self):
        return f'Build_Procedure({", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        raise Exception('Procedures are not implemented')

class Method(DescriptorR):
    
    def __init__(self, time_out=None, method=None, device=None):
        super().__init__(
            dscptrs=[time_out, method, device],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_METHOD,
            )
        )

    @property
    def time_out(self):
        return self._dscptrs[0]

    @property
    def method(self):
        return self._dscptrs[1]

    @property
    def device(self):
        return self._dscptrs[2]

    def __repr__(self):
        return f'Build_Method({", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        raise Exception('Methods are not implemented')

class Dependency(DescriptorR):
    
    def __init__(self, treedep=0, *arguments):
        super().__init__(
            data=numpy.uint8(treedep),
            dscptrs=[*arguments],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_DEPENDENCY,
            )
        )

    @property
    def treedep(self):
        return self._data

    @property
    def arguments(self):
        return self._dscptrs

    def __repr__(self):
        return f'Build_Dependency({self._data}, {", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        raise Exception('Dependencies are not implemented')

class Condition(DescriptorR):
    
    def __init__(self, treecond=0, condition=None):
        super().__init__(
            data=numpy.uint8(treecond),
            dscptrs=[condition],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_CONDITION,
            )
        )

    @property
    def treecond(self):
        return self._data

    @property
    def condition(self):
        return self._dscptrs[0]

    def __repr__(self):
        return f'Build_Condition({self._data}, {", ".join(map(repr, self._dscptrs))})'

class WithUnits(DescriptorR):
    
    def __init__(self, value=None, units=None):
        super().__init__(
            dscptrs=[value, units],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_WITH_UNITS,
            )
        )

    @property
    def value(self):
        return self._dscptrs[0]

    @property
    def units(self):
        return self._dscptrs[1]

    def __repr__(self):
        return f'Build_With_Units({", ".join(map(repr, self._dscptrs))})'

    def data(self):
        return self.value.data()

class Call(DescriptorR):
    
    def __init__(self, return_dtype_id=DTYPE_L, image=None, routine=None, *arguments):
        super().__init__(
            data=numpy.uint8(return_dtype_id),
            dscptrs=[image, routine, *arguments],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_CALL,
            )
        )

    @property
    def return_dtype_id(self):
        return self._data

    @property
    def image(self):
        return self._dscptrs[0]
    
    @property
    def routine(self):
        return self._dscptrs[1]
    
    @property
    def arguments(self):
        return self._dscptrs[2 : ]

    def __repr__(self):
        return f'Build_Call({self._data}, {", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        raise Exception('Calls are not implemented')

class WithError(DescriptorR):
    
    def __init__(self, value=None, error=None):
        super().__init__(
            dscptrs=[value, error],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_WITH_ERROR,
            )
        )

    @property
    def value(self):
        return self._dscptrs[0]

    @property
    def error(self):
        return self._dscptrs[1]

    def __repr__(self):
        return f'Build_With_Error({", ".join(map(repr, self._dscptrs))})'
    
    def getException(self):
        return getExceptionFromError(self.error.data())

    def data(self):
        return self.value.data()

class Opaque(DescriptorR):
    
    def __init__(self, value=None, opaque_type=None):
        super().__init__(
            dscptrs=[value, opaque_type],
            dsc=mdsdsc_r_t(
                dtype_id=DTYPE_OPAQUE,
            )
        )

    @property
    def value(self):
        return self._dscptrs[0]

    @property
    def opaque_type(self):
        return self._dscptrs[1]

    def __repr__(self):
        return f'Build_Opaque({", ".join(map(repr, self._dscptrs))})'
    
    def data(self):
        return self.value.data()

###
### Lookup Tables
###

CLASS_MAP = {
    CLASS_MISSING: Descriptor,
    CLASS_S: DescriptorS,
    CLASS_A: DescriptorA,
    CLASS_CA: DescriptorA,
    CLASS_APD: DescriptorA,
    CLASS_R: DescriptorR,
}

DTYPE_CLASS_MAP = {
    CLASS_S: {
        CLASS_MISSING: Descriptor,
        DTYPE_T: String,
        DTYPE_IDENT: Ident,
        DTYPE_PATH: TreePath,
        DTYPE_NID: TreeNID,
        DTYPE_BU: UInt8,
        DTYPE_WU: UInt16,
        DTYPE_LU: UInt32,
        DTYPE_QU: UInt64,
        DTYPE_B: Int8,
        DTYPE_W: Int16,
        DTYPE_L: Int32,
        DTYPE_Q: Int64,
        DTYPE_FS: Float32,
        DTYPE_F: Float32,
        DTYPE_FT: Float64,
        DTYPE_D: Float64,
        DTYPE_G: Float64,
    },
    CLASS_A: {
        CLASS_MISSING: Descriptor,
        DTYPE_T: StringArray,
        DTYPE_BU: UInt8Array,
        DTYPE_WU: UInt16Array,
        DTYPE_LU: UInt32Array,
        DTYPE_QU: UInt64Array,
        DTYPE_B: Int8Array,
        DTYPE_W: Int16Array,
        DTYPE_L: Int32Array,
        DTYPE_Q: Int64Array,
        DTYPE_FS: Float32Array,
        DTYPE_F: Float32Array,
        DTYPE_FT: Float64Array,
        DTYPE_D: Float64Array,
        DTYPE_G: Float64Array,
    },
    CLASS_APD: {
        DTYPE_LIST: List,
        DTYPE_TUPLE: Tuple,
        DTYPE_DICTIONARY: Dictionary,
    },
    CLASS_R: {
        CLASS_MISSING: Descriptor,
        DTYPE_SIGNAL: Signal,
        DTYPE_DIMENSION: Dimension,
        DTYPE_WINDOW: Window,
        DTYPE_SLOPE: Slope,
        DTYPE_FUNCTION: Function,
        DTYPE_CONGLOM: Conglom,
        DTYPE_RANGE: Range,
        DTYPE_ACTION: Action,
        DTYPE_DISPATCH: Dispatch,
        DTYPE_PROGRAM: Program,
        DTYPE_ROUTINE: Routine,
        DTYPE_PROCEDURE: Procedure,
        DTYPE_METHOD: Method,
        DTYPE_DEPENDENCY: Dependency,
        DTYPE_CONDITION: Condition,
        DTYPE_WITH_UNITS: WithUnits,
        DTYPE_CALL: Call,
        DTYPE_WITH_ERROR: WithError,
        DTYPE_OPAQUE: Opaque,
    }
}

NUMPY_DTYPE_MAP = {
    DTYPE_BU: numpy.uint8,
    DTYPE_WU: numpy.uint16,
    DTYPE_LU: numpy.uint32,
    DTYPE_QU: numpy.uint64,
    DTYPE_B: numpy.int8,
    DTYPE_W: numpy.int16,
    DTYPE_L: numpy.int32,
    DTYPE_Q: numpy.int64,
    DTYPE_FS: numpy.float32,
    DTYPE_FT: numpy.float64,
    DTYPE_NID: numpy.uint32,
}
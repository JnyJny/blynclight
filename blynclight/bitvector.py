"""a vector.. of bits!
"""

import functools
import operator

from typing import List, Union

from loguru import logger


class BitField:
    """Data Descriptor for accessing named fields in a BitVector.

    class MyBV(BitVector):
        ...
        byte0 = BitField(0, 8)
        byte1 = BitField(8, 8)
        bit16 = BitField(16)
        bit17 = BitField(17)
        pad0  = BitField(18, 4)
        byte3 = BitField(32, 8)
    
    > mybv = MyBV()
    > mybv.byte0 = 0xff
    > mybv.bit17 = 1
    > mybv.byte3 = 0x55
    > mybv
    MyBV(value=0x5502ff, length=128)

    """

    def __init__(self, offset: int, width: int = 1):
        """
        :param offset: int
        :param width: int
        """
        self.field = slice(offset, offset + width)

    def __get__(self, obj, type=None) -> int:

        value = obj[self.field]
        logger.debug(f"get {self.name} -> {value}")
        return value

    def __set__(self, obj, value) -> None:
        prev = obj[self.field]
        logger.debug(f"set {self.name}[{self.field}] {prev} -> {value}")
        obj[self.field] = value

    def __set_name__(self, owner, name) -> None:
        self.name = name


@functools.total_ordering
class BitVector:
    """A Bit Vector is a list of bits in packed (integer)
    format that can be accessed by indexing into the vector
    or using a slice (via conventional square brackets 
    notation). 

    """

    def __init__(self, value: int = 0, size: int = 128):
        self.MAX = (1 << size) - 1
        self.value: int = value & self.MAX

    def _getb(self, offset: int) -> int:
        """Retrieves the bit value at offset."""
        return (self.value >> offset) & 0x1

    def _setb(self, offset: int) -> None:
        """Sets the bit value at offset."""
        self.value |= (1 << offset) & self.MAX

    def _clrb(self, offset: int) -> None:
        """Clears the bit value at offset."""
        self.value &= ~(1 << offset)

    def _setval(self, offset: int, value: int):
        if value:
            self._setb(offset)
        else:
            self._clrb(offset)

    def toggle(self, offset: int) -> int:
        """Toggle the bit at offset in the vector and return the previous value.
        """
        prev = self._getb(offset)
        self.value ^= (1 << offset) & self.MAX
        return prev

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self!s}, size={len(self)})"

    def __str__(self) -> str:
        nibbles = (len(self) // 4) + 1 if (len(self) % 4) else 0
        hexstr = "0x{{:0{0}x}}".format(nibbles)
        return hexstr.format(self.value)

    def __len__(self) -> int:
        """Length of the vector in bits."""
        try:
            return self._len
        except AttributeError:
            pass
        self._len = self.MAX.bit_length()
        return self._len

    def __getitem__(self, key: Union[int, slice]) -> int:
        """Given a key, retrieve a bit or bitfield."""
        try:
            return self._getb(key & (len(self) - 1))
        except TypeError:
            pass

        value = 0
        for n, b in enumerate(range(*key.indices(len(self)))):
            v = self._getb(b)
            if v:
                value += 1 << n
        return value

    def __setitem__(self, key: Union[int, slice], value: Union[int, bool]) -> None:
        """Given a key, set a bit or bitfield to the supplied value.

        If value is True or False and the key is a slice describing a
        bit field, each bit in the field takes on the value.  Otherwise,
        the value is left shifted and the lsb is added to the next offset
        in the bit field.

        > b[:8] = True   # results in b0 - b7 == 1
        > b[:7] = 0x1    # results in b0 == 1 and the rest of the bits == 0
        
        The difference is subtle and perhaps should not be considered a feature.
        """
        try:
            if key < 0:
                key += len(self)

            self._setval(key, value)
            return

        except TypeError:
            pass

        try:
            if value is True or value is False:
                for b in range(*key.indices(len(self))):
                    self._setval(b, value)
                return

            for n, b in enumerate(range(*key.indices(len(self)))):
                self._setval(b, (value >> n) & 0x1)

        except AttributeError:
            raise ValueError("Expected int or slice key") from None

    def __binary_op(self, other, func, return_obj: bool = False, reverse: bool = False):
        """Calls the supplied function `func` with self and other.

        If the user sets return_obj to True, a new BitVector initialized with the
        results of `func` is returned.  If `reverse` is True, the order of self and other
        is reversed in the call to `func`.

        :param other: Union[int, BitVector]
        :param func: callable from operator
        :param return_obj: bool
        :param reverse: bool
        :return: Union[int, bool, BitVector]
        """
        a, b = (self, other) if not reverse else (other, self)

        try:
            retval = func(a.value, b.value)
            if return_obj:
                retval = self.__class__(retval)
            return retval
        except AttributeError:
            pass

        retval = func(a.value, b)
        if return_obj:
            retval = self.__class__(retval)
        return retval

    def __unary_op(self, func, return_obj: bool = False):
        """Calls the supplied function `func` with self and returns the result.

        If return_obj is True, the return value is a BitVector initialized from
        the results of `func`. 

        :param func: callable from operator 
        :param return_obj: bool
        :return: Union[int, BitVector]
        """

        retval = func(self.value) & self.MAX
        if return_obj:
            retval = self.__class__(retval)
        return retval

    def __inplace_op(self, other, func) -> object:
        """Calls the supplied binary function `func` with self and other
        and updates self with the results. 

        :param other:  Union[int, BitVector]
        :param func: Callable from operator
        :return: self
        """
        try:
            self.value = func(self.value, other.value) & self.MAX
        except AttributeError:
            pass
        self.value = func(self.value, other) & self.MAX
        return self

    def bin(self) -> str:
        """Binary string representation of BitVector."""
        return bin(self.value)

    def hex(self) -> str:
        """Hexadecimal string representation of BitVector."""
        return hex(self.value)

    @property
    def bytes(self) -> bytes:
        """Bytes representation of BitVector."""
        n = len(self) // 8 + (1 if len(self) % 8 else 0)
        return self.value.to_bytes(n, "big")

    __eq__ = functools.partialmethod(__binary_op, func=operator.eq)
    __gt__ = functools.partialmethod(__binary_op, func=operator.gt)

    __add__ = functools.partialmethod(__binary_op, func=operator.add)
    __radd__ = functools.partialmethod(__binary_op, func=operator.add, reverse=True)
    __iadd__ = functools.partialmethod(__inplace_op, func=operator.add)

    __sub__ = functools.partialmethod(__binary_op, func=operator.sub)
    __rsub__ = functools.partialmethod(__binary_op, func=operator.sub, reverse=True)
    __isub__ = functools.partialmethod(__inplace_op, func=operator.sub)

    __mul__ = functools.partialmethod(__binary_op, func=operator.mul)
    __rmul__ = functools.partialmethod(__binary_op, func=operator.mul, reverse=True)
    __imul__ = functools.partialmethod(__inplace_op, func=operator.mul)

    __and__ = functools.partialmethod(__binary_op, func=operator.and_)
    __rand__ = functools.partialmethod(__binary_op, func=operator.and_, reverse=True)
    __iand__ = functools.partialmethod(__inplace_op, func=operator.and_)

    __or__ = functools.partialmethod(__binary_op, func=operator.or_)
    __ror__ = functools.partialmethod(__binary_op, func=operator.or_, reverse=True)
    __ior__ = functools.partialmethod(__inplace_op, func=operator.or_)

    __or__ = functools.partialmethod(__binary_op, func=operator.or_)
    __ror__ = functools.partialmethod(__binary_op, func=operator.or_, reverse=True)
    __ior__ = functools.partialmethod(__inplace_op, func=operator.or_)

    __xor__ = functools.partialmethod(__binary_op, func=operator.xor)
    __rxor__ = functools.partialmethod(__binary_op, func=operator.xor, reverse=True)
    __ixor__ = functools.partialmethod(__inplace_op, func=operator.xor)

    __not__ = functools.partialmethod(__unary_op, operator.not_, return_obj=True)
    __invert__ = functools.partialmethod(__unary_op, operator.invert, return_obj=True)
    __neg__ = functools.partialmethod(__unary_op, operator.neg, return_obj=True)
    __pos__ = functools.partialmethod(__unary_op, operator.pos, return_obj=True)

    __lshift__ = functools.partialmethod(__binary_op, operator.lshift, return_obj=True)
    __ilshift__ = functools.partialmethod(__inplace_op, operator.lshift)

    __rshift__ = functools.partialmethod(__binary_op, operator.rshift, return_obj=True)
    __irshift__ = functools.partialmethod(__inplace_op, operator.rshift)

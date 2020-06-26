"""a vector.. of bits!
"""

import functools
import operator

from typing import List, Union

from loguru import logger


class BitField:
    """Data Descriptor for naming fields in a BitVector.
    """

    def __init__(self, offset: int, width: int = 1):
        """
        :param offset: int
        :param width: int [defaults to 1]
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
    def __init__(self, value: int = 0, size: int = 128):
        self.MAX = (1 << size) - 1
        self.value: int = value & self.MAX

    def _getb(self, bit: int) -> int:

        return (self.value >> bit) & 0x1

    def _setb(self, bit: int) -> None:

        self.value |= (1 << bit) & self.MAX

    def _clrb(self, bit: int) -> None:

        self.value &= ~(1 << bit)

    def _setval(self, bit: int, value: int):
        if value:
            self._setb(bit)
        else:
            self._clrb(bit)

    def toggle(self, bit: int) -> int:
        """Toggle the n-th `bit` in the vector and return it's previous value.
        """
        self.value ^= (1 << bit) & self.MAX
        return not self._getb(bit)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self!s}, size={len(self)})"

    def __str__(self) -> str:
        hexstr = "0x{{:0{0}x}}".format(len(self) // 4)
        return hexstr.format(self.value)

    def __len__(self) -> int:
        """Length of the bit vector in bits."""
        try:
            return self._len
        except AttributeError:
            pass
        self._len = bin(self.MAX).count("1")
        return self._len

    def __getitem__(self, key: Union[int, slice]) -> int:

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
        """
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

        retval = func(self.value) & self.MAX
        if return_obj:
            retval = self.__class__(retval)
        return retval

    def __inplace_op(self, other, func):
        try:
            self.value = func(self.value, other.value) & self.MAX
        except AttributeError:
            pass
        self.value = func(self.value, other) & self.MAX
        return self

    def bin(self) -> str:
        return bin(self.value)

    def hex(self) -> str:
        return hex(self.value)

    @property
    def bytes(self) -> bytes:
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

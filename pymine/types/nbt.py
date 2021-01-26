from __future__ import annotations

from mutf8 import encode_modified_utf8, decode_modified_utf8

from pymine.types.buffer import Buffer

TYPES = (TAG_End, TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double, TAG_Byte_Array, TAG_String, TAG_List)


class TAG:
    """Base class for an NBT tag.

    :param str name: Name of the tag.
    :attr int id: The type ID.
    :attr name
    """

    id = None

    def __init__(self, name: str = None) -> None:
        self.id = self.__class__.id
        self.name = name

    def encode_meta(self) -> bytes:
        mutf8_name = encode_modified_utf8(self.name)
        return Buffer.pack("b", self.id) + Buffer.pack("H", len(mutf8_name)) + mutf8_name

    @staticmethod
    def meta_from_buf(buf: Buffer) -> tuple:  # returns the type id and name
        return buf.unpack("b"), decode_modified_utf8(buf.read(buf.unpack("H")))

    def encode_value(self) -> bytes:
        raise NotImplementedError

    def encode(self) -> bytes:
        raise NotImplementedError

    @staticmethod
    def value_from_buf(buf: Buffer) -> NotImplemented:
        raise NotImplementedError

    @classmethod
    def from_buf(cls, buf: Buffer) -> NotImplemented:
        raise NotImplementedError


class TAG_End(TAG):
    """Used to represent a TAG_End, signifies the end of a TAG_Compound."""

    id = 0

    def __init__(self) -> None:
        super().__init__()

    def encode(self) -> bytes:
        return b"\x00"

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_End:
        assert buf.unpack("b") == b"\x00"
        return cls()


class TAG_Byte(TAG):
    """Used to represent a TAG_Byte, stores a single signed byte.

    :param int value: A signed byte.
    :attr value:
    """

    id = 1

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)

        self.value = value

    def encode_value(self) -> bytes:
        return Buffer.pack("b", self.value)

    def encode(self) -> bytes:
        return self.encode_meta() + self.encode_value()

    @staticmethod
    def value_from_buf(buf: Buffer) -> int:
        return buf.unpack("b")

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_Byte:
        return cls(cls.decode_meta(buf)[1], cls.value_from_buf(buf))


class TAG_Short(TAG):
    """Used to represent a TAG_Short, stores a single short (2 byte int).

    :param int value: A short (number).
    :attr value:
    """

    id = 2

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("h", self.value)

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_Short:
        return cls(buf.unpack("h"))


class TAG_Int(TAG):
    """Used to represent a TAG_Int, stores a single integer (4 bytes).

    :param int value: An integer.
    :attr value:
    """

    id = 3

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("i", self.value)

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_Int:
        return cls(buf.unpack("i"))


class TAG_Long(TAG):
    """Used to represent a TAG_Long, stores a long long (8 byte integer).

    :param int value: A long long (number).
    :attr value:
    """

    id = 4

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("q", self.value)

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_Long:
        return cls(buf.unpack("q"))


class TAG_Float(TAG):
    """Used to represent a TAG_Float, stores a float (4 bytes).

    :param float value: A float (number).
    :attr value:
    """

    id = 5

    def __init__(self, name: str, value: float) -> None:
        super().__init__(name)

        self.value = value

    def from_buf(self) -> bytes:
        return Buffer.pack("f", self.value)

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_Float:
        return cls(buf.unpack("f"))


class TAG_Double(TAG):
    """Used to represent a TAG_Double, stores a double (8 byte float).

    :param float value: A double (number).
    :attr value:
    """

    id = 6

    def __init__(self, name: str, value: float) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("d", self.value)

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_Double:
        return cls(buf.unpack("d"))


class TAG_Byte_Array(TAG):
    """Used to represent a TAG_Byte_Array, stores an array of bytes.

    :param bytes value: Some bytes.
    :attr value:
    """

    id = 7

    def __init__(self, name: str, value: bytes) -> None:
        super().__init__(name)

        self.value = bytearray(value)

    def encode(self) -> bytes:
        return Buffer.pack("i", len(self.value)) + Buffer.pack_array("b", self.value)

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_Byte_Array:
        return cls(buf.unpack_array("b", buf.unpack("i")))


class TAG_String(TAG):
    """Used to represent a TAG_String, stores a string.

    :param str value: A string
    :attr value:
    """

    id = 8

    def __init__(self, name: str, value: str) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        utf8 = self.value.encode("utf8")
        return Buffer.pack("h", len(utf8)) + utf8

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_String:
        return cls(buf.read(buf.unpack("h")).decode("utf8"))


class TAG_List(TAG):
    """Packs a list of other tags, the tags in the array are nameless and typeless.

    :param str name: The name of the TAG
    :param list value: A uniform list of TAGs
    """

    def __init__(self, name: str, value: list) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return (
            Buffer.pack("b", self.value[0].id)
            + Buffer.pack("i", len(self.value))
            + b"".join([value.encode() for value in self.value])
        )

    @classmethod
    def from_buf(cls, buf: Buffer) -> TAG_List:
        type_id = buf.unpack("b")
        return cls([TYPES[type_id].from_buf(buf) for _ in range(buf.unpack("i"))])

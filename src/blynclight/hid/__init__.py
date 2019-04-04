""" Human Input Device

This module provides a ctypes interface to the hidapi
C language library. 

"""

import ctypes
import ctypes.util
import atexit

__all__ = ["HidDevice"]


class DeviceInfo(ctypes.Structure):
    """DeviceInfo is the return data-type of hidapi.hid_enumerate.
    """

    def as_dict(self) -> dict:
        """Translate DeviceInfo to a dictionary whose keys are the structure's
        field names and the values are the corresponding field values.
        """
        info = {}
        for name, typ in self._fields_:
            if name == "next":
                continue
            info[name] = getattr(self, name, None)
        return info


DeviceInfo._fields_ = [
    ("path", ctypes.c_char_p),
    ("vendor_id", ctypes.c_ushort),
    ("product_id", ctypes.c_ushort),
    ("serial_number", ctypes.c_wchar_p),
    ("release_number", ctypes.c_ushort),
    ("manufacturer_string", ctypes.c_wchar_p),
    ("product_string", ctypes.c_wchar_p),
    ("usage_page", ctypes.c_ushort),
    ("usage", ctypes.c_ushort),
    ("interface_number", ctypes.c_int),
    ("next", ctypes.POINTER(DeviceInfo)),
]


class Device(ctypes.Structure):
    """An opaque handle returned by hidapi.hid_open and used
    as an argument in the functions:
    hidapi.hid_read
    hidapi.hid_read_timeout
    hidapi.hid_write
    """

    pass


_hidapi_libraries = [
    "hidapi",
    "hidapi-hidraw",
    "hidapi-libusb",
    "hidapi-iohidmanager",
]

for stem in _hidapi_libraries:
    fullname = ctypes.util.find_library(stem)
    if fullname:
        hidapi = ctypes.cdll.LoadLibrary(fullname)
        break
else:
    raise ImportError("failed to locate hidapi shared object")

hidapi.hid_enumerate.argstype = [ctypes.c_ushort, ctypes.c_ushort]
hidapi.hid_enumerate.restype = ctypes.POINTER(DeviceInfo)

hidapi.hid_free_enumeration.argstype = [ctypes.POINTER(DeviceInfo)]
hidapi.hid_free_enumeration.restype = None

hidapi.hid_open.argstype = [ctypes.c_ushort, ctypes.c_ushort, ctypes.c_wchar_p]
hidapi.hid_open.restype = ctypes.POINTER(Device)

hidapi.hid_open_path.argstype = [ctypes.c_char_p]
hidapi.hid_open_path.restype = ctypes.POINTER(Device)

hidapi.hid_close.argstype = [ctypes.POINTER(Device)]
hidapi.hid_close.restype = None

hidapi.hid_write.argstype = [
    ctypes.POINTER(Device),
    ctypes.POINTER(ctypes.c_byte),
    ctypes.c_size_t,
]
hidapi.hid_write.restype = ctypes.c_int

hidapi.hid_read.argstype = [
    ctypes.POINTER(Device),
    ctypes.POINTER(ctypes.c_byte),
    ctypes.c_size_t,
]
hidapi.hid_read.restype = ctypes.c_int

hidapi.hid_read_timeout.argstype = [
    ctypes.POINTER(Device),
    ctypes.POINTER(ctypes.c_byte),
    ctypes.c_size_t,
    ctypes.c_int,
]
hidapi.hid_read_timeout.restype = ctypes.c_int

hidapi.hid_init()
atexit.register(hidapi.hid_exit)


class HidDevice:
    """A USB Human Input Device (HID) Device
    
    Provides read and write access to devices that adhere to the USB
    HID protocol. The enumerate class method can be used to discover
    currently attached devices.

    """

    _opened = set()

    @classmethod
    def enumerate(cls, vendor_id: int = 0, product_id: int = 0) -> list:
        """Returns a list of dictionaries describing USB devices.  Specifying
        vendor_id and product_id will only return devices whose
        vendor_id or product_id match the ones given. If no USB devices are
        found, an empty list is returned. See hid.DeviceInfo for more
        information on the contents of the dictionary.

        :param vendor_id: optional integer
        :param product_id: optional integer
        :return: list

        """
        devices = []
        head = hidapi.hid_enumerate(vendor_id, product_id)
        cursor = head
        while cursor:
            devices.append(cursor.contents.as_dict())
            cursor = cursor.contents.next
        hidapi.hid_free_enumeration(head)
        return devices

    @classmethod
    def from_dict(cls, info: dict):
        """Returns a configured hid.HidDevice object from a
        DeviceInfo-derived dictionary.

        :param info: dictionary
        :return: hid.HidDevice
        """
        return cls(info["vendor_id"], info["product_id"])

    def __init__(self, vendor_id, product_id, path=None):
        """
        :param vendor_id: 16-bit integer quantity
        :param product_id: 16-bit integer quantity
        :param path: optional string

        Raises ValueError if the vendor_id:product_id pair
        specifies a device that is already open.
        """
        self.vendor_id = vendor_id & 0xFFFF
        self.product_id = product_id & 0xFFFF
        self.path = path
        # XXX this a hack to keep from inducing a crash in libhidapi
        #     hid_open should return NULL instead of crashing.
        if self.identifier in self._opened:
            raise ValueError(
                f"{self.__class__.__name__} {self.identifier} already in use"
            )
        self._opened.add(self.identifier)

    def __del__(self):
        """The hid.HidDevice is closed when the object is deleted.
        """
        self.close()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(vendor_id=0x{self.vendor_id:04x},"
            f"product_id=0x{self.product_id:04x})"
        )

    @property
    def identifier(self):
        """A string concatenation of the vendor and product identifiers.
        e.g. 0xff11:0x0001
        """
        try:
            return self._identifier
        except AttributeError:
            pass
        self._identifier = f"0x{self.vendor_id:04x}:0x{self.product_id:04x}"
        return self._identifier

    @property
    def handle(self):
        """An opaque hid.Device structure pointer used
        to specify the device for I/O operations.
        """
        try:
            return self._handle
        except AttributeError:
            pass
        self._handle = hidapi.hid_open(
            self.vendor_id, self.product_id, self.path
        )
        return self._handle

    def close(self):
        """Closes the hidapi handle and sets the handle attribute to None.
        """
        hidapi.hid_close(self.handle)
        self._handle = None
        self._opened.discard(self.identifier)

    def write(self, data: bytes) -> int:
        """Writes data to the device.

        :param data: bytes buffer of data
        :return: number of bytes written
        """
        return hidapi.hid_write(self.handle, data, len(data))

    def read(self, data: bytes, timeout: int = None) -> int:
        """Reads data from the device into the given bytes buffer.

        :param data: bytes buffer
        :param timeout: optional timeout in milliseconds
        :return: integer bytes read
        """
        if timeout:
            return hidapi.hid_read_timeout(
                self.handle, data, len(data), timeout
            )
        return hidapi.hid_read(self.handle, data, len(data))

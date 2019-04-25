"""Human Input Device

This module provides a ctypes interface to the USB hidapi C language
library. Functions exposed for use by python via ctypes are:

- void  hid_init(void)
- void  hid_exit(void)
- void *hid_enumerate(int, int)
- void  hid_free_enumeration(void *)
- void *hid_open(int, int)
- void *hid_open_path(char *)
- void  hid_close(void *)
- uint  hid_write(void *, uchar_t *, size_t)
- uint  hid_read(void *, uchar_t *, size_t)
- uint  hid_read_timeout(void, uchar_t *, size_t, int)


The HidDevice class encapsulates all of these functions (with the
exception of hid_init and hid_exit) and provides a more pythonic
interface e.g.:

> from hid import HidDevice
> all_devices = HidDevice.enumerate()
> first_device = HidDevice.from_dict(all_devices[0])
> d = HidDevice(0xe0e0, 0x0001)
> buf = bytes([0xff, 0, 0, 0xff])
> d.write(buf)
4


The hidapi library setup and teardown is done for the user; hid_init()
is called when the module is imported and hid_exit() is scheduled to be
called on process exit using the atexit module.

"""

import ctypes
import ctypes.util
import atexit

__all__ = ["HidDevice"]


class _DeviceInfo(ctypes.Structure):
    """_DeviceInfo is the return data-type of hidapi.hid_enumerate.
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


# the _fields_ array is defined after declaring the class because
# this structure has a 'next' pointer in it that of type DeviceInfo
# and the ctypes.Structure class can't handle self-referencing
# pointers.

_DeviceInfo._fields_ = [
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
    ("next", ctypes.POINTER(_DeviceInfo)),
]


class _DeviceHandle(ctypes.Structure):
    """An opaque handle returned by hidapi.hid_open and used
    as an argument in the functions:
    hidapi.hid_read
    hidapi.hid_read_timeout
    hidapi.hid_write
    """

    pass


_hidapi_libraries = ["hidapi", "hidapi-hidraw", "hidapi-libusb", "hidapi-iohidmanager"]

for stem in _hidapi_libraries:
    fullname = ctypes.util.find_library(stem)
    if fullname:
        hidapi = ctypes.cdll.LoadLibrary(fullname)
        break
else:
    raise ImportError("failed to locate hidapi shared object")

_function_signatures = [
    ("hid_enumerate", [ctypes.c_ushort, ctypes.c_ushort], ctypes.POINTER(_DeviceInfo)),
    ("hid_free_enumeration", [ctypes.POINTER(_DeviceInfo)], None),
    (
        "hid_open",
        [ctypes.c_ushort, ctypes.c_ushort, ctypes.c_wchar_p],
        ctypes.POINTER(_DeviceHandle),
    ),
    ("hid_open_path", [ctypes.c_char_p], ctypes.POINTER(_DeviceHandle)),
    ("hid_close", [ctypes.POINTER(_DeviceHandle)], None),
    (
        "hid_write",
        [ctypes.POINTER(_DeviceHandle), ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t],
        ctypes.c_int,
    ),
    (
        "hid_read",
        [ctypes.POINTER(_DeviceHandle), ctypes.POINTER(ctypes.c_byte), ctypes.c_size_t],
        ctypes.c_int,
    ),
    (
        "hid_read_timeout",
        [
            ctypes.POINTER(_DeviceHandle),
            ctypes.POINTER(ctypes.c_byte),
            ctypes.c_size_t,
            ctypes.c_int,
        ],
        ctypes.c_int,
    ),
]

for fname, argstype, restype in _function_signatures:
    function = getattr(hidapi, fname)
    function.argstype = argstype
    function.restype = restype

hidapi.hid_init()
atexit.register(hidapi.hid_exit)


class HidDevice:
    """A USB Human Input Device (HID) Device

    Provides read and write access to devices that adhere to the USB
    HID protocol. The HidDevice.enumerate class method can be used to
    discover currently attached devices.

    """

    _opened = set()

    @classmethod
    def enumerate(cls, vendor_id: int = 0, product_id: int = 0) -> list:
        """Returns a list of dictionaries describing USB devices.  Specifying
        vendor_id and product_id will only return devices whose
        vendor_id or product_id match the ones given. If no USB devices are
        found, an empty list is returned. See hid._DeviceInfo for more
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

        try:
            return cls(info["vendor_id"], info["product_id"])
        except KeyError:
            raise LookupError("dictionary missing vendor_id or product_id key")

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
        # XXX this a hack to keep from re-opening a USB device and
        #     inducing a crash in libhidapi.

        if self.identifier in self._opened:
            raise ValueError(f"{self.identifier} already in use")
        self._opened.add(self.identifier)

    def __del__(self):
        """The hid.HidDevice is closed when the object is deleted.
        """
        self.close()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(vendor_id=0x{self.vendor_id:04x},"
            f"product_id=0x{self.product_id:04x},"
            f"path={self.path})"
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
        """An opaque hid._DeviceHandle structure pointer used
        to specify the device for I/O operations.
        """
        try:
            return self._handle
        except AttributeError:
            pass
        self._handle = hidapi.hid_open(self.vendor_id, self.product_id, self.path)
        if not self._handle:
            raise LookupError(f"no such device: {self.identifier}")
        self._opened.add(self.identifier)
        return self._handle

    def close(self):
        """Closes the hidapi handle and sets the handle attribute to None.
        """
        # Avoid using the handle getter method here, use _handle
        # instead.  Otherwise we can crash the process with an
        # unintentional SIGSEGV or SIGFAULT while we are shutting
        # things down.
        try:
            if self._handle:
                hidapi.hid_close(self._handle)
        except AttributeError:
            pass
        self._handle = None
        self._opened.discard(self.identifier)

    def write(self, data: bytes) -> int:
        """Write data to the device.

        :param data: bytes buffer of data
        :return: number of bytes written
        """
        return hidapi.hid_write(self.handle, data, len(data))

    def read(self, nbytes: int, timeout: int = None) -> bytes:
        """Reads data from the device into the given bytes buffer.

        :param nbytes: integer
        :param timeout: optional timeout in milliseconds
        :return: bytes read
        """

        buf = (ctypes.c_ubyte * nbytes)()

        if timeout:
            hidapi.hid_read_timeout(self.handle, buf, nbytes, timeout)
        else:
            hidapi.hid_read(self.handle, buf, nbytes)
        return bytearray(buf)

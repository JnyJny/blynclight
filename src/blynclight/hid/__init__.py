'''
'''

import ctypes
import ctypes.util
import platform
import atexit

__all__ = [ 'enumerate', 'open', 'read', 'write', 'close' ]

class DeviceInfo(ctypes.Structure):
    def as_dict(self):
        ret = {}
        for name, ftype in self._fields_:
            if name == 'next':
                continue
            ret[name] = getattr(self, name, None)
        return ret

DeviceInfo._fields_ = [
    ('path', ctypes.c_char_p),
    ('vendor_id', ctypes.c_ushort),
    ('product_id', ctypes.c_ushort),
    ('serial_number', ctypes.c_wchar_p),
    ('release_number', ctypes.c_ushort),
    ('manufacturer_string', ctypes.c_wchar_p),
    ('product_string', ctypes.c_wchar_p),
    ('usage_page', ctypes.c_ushort),
    ('usage', ctypes.c_ushort),
    ('interface_number', ctypes.c_int),
    ('next', ctypes.POINTER(DeviceInfo)),
]

class Device(ctypes.Structure):
    pass

hidapi_libraries = ['hidapi',
                    'hidapi-hidraw',
                    'hidapi-libusb',
                    'hidapi-iohidmanager']

for stem in hidapi_libraries:
    fullname = ctypes.util.find_library(stem)
    if fullname:
        hidapi = ctypes.cdll.LoadLibrary(fullname)
        break
else:
    raise ImportError('failed to locate suitable hidapi shared object')


hidapi.hid_enumerate.argstype = [ctypes.c_ushort, ctypes.c_ushort]
hidapi.hid_enumerate.restype = ctypes.POINTER(DeviceInfo)

hidapi.hid_free_enumeration.argstype = [ctypes.POINTER(DeviceInfo)]
hidapi.hid_free_enumeration.restype = None

hidapi.hid_open.argstype = [ctypes.c_ushort, 
                            ctypes.c_ushort,
                            ctypes.c_wchar_p]
hidapi.hid_open.restype = ctypes.POINTER(Device)

hidapi.hid_open_path.argstype = [ctypes.c_char_p]
hidapi.hid_open_path.restype = ctypes.POINTER(Device)

hidapi.hid_close.argstype = [ctypes.POINTER(Device)]
hidapi.hid_close.restype = None

hidapi.hid_write.argstype = [ctypes.POINTER(Device),
                             ctypes.POINTER(ctypes.c_byte),
                             ctypes.c_size_t]
hidapi.hid_write.restype = ctypes.c_int

hidapi.hid_read.argstype = [ctypes.POINTER(Device),
                            ctypes.POINTER(ctypes.c_byte),
                            ctypes.c_size_t]
hidapi.hid_read.restype = ctypes.c_int

hidapi.hid_read_timeout.argstype = [ctypes.POINTER(Device),
                                    ctypes.POINTER(ctypes.c_byte),
                                    ctypes.c_size_t,
                                    ctypes.c_int]
hidapi.hid_read_timeout.restype = ctypes.c_int

hidapi.hid_init()
atexit.register(hidapi.hid_exit)

def enumerate(vendor_id: int =0, product_id: int = 0):
    devices = []
    head = hidapi.hid_enumerate(vendor_id, product_id)
    cursor = head
    while cursor:
        devices.append(cursor.contents.as_dict())
        cursor = cursor.contents.next
    hidapi.hid_free_enumeration(head)
    return devices

def open(vendor_id: int, product_id: int):
    '''
    
    '''
    
    return hidapi.hid_open(vendor_id, product_id, None)
    

def write(handle: Device, data: ctypes.c_ubyte , ndata: int):
    
    return hidapi.hid_write(handle, data, ndata)

def read(handle, data, timeout=None):
    
    ndata = ctypes.sizeof(data)

    if timeout:
        return hidapi.hid_read_timeout(handle, data, ndata, timeout)

    return hidapi.hid_read(handle, data, ndata)

def close(handle):

    hidapi.hid_close(handle)
    


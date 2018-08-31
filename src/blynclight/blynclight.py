'''Embrava Blynclight Support
'''

import ctypes
from .constants import FlashSpeed, DeviceType, MusicVolume
from .hid import enumerate as hid_enumerate
from .hid import write as hid_write
from .hid import open as hid_open
from .hid import read as hid_read
from .hid import close as hid_close


class BlyncLightStatus(ctypes.Structure):
    _fields_ = [('pad0', ctypes.c_uint64, 56),
                ('report', ctypes.c_uint64, 8),
                ('red', ctypes.c_uint64, 8),
                ('blue', ctypes.c_uint64, 8),
                ('green', ctypes.c_uint64, 8),
                ('off', ctypes.c_uint64, 1),
                ('dim', ctypes.c_uint64, 1),
                ('flash', ctypes.c_uint64, 1),
                ('speed', ctypes.c_uint64, 3),
                ('pad1', ctypes.c_uint64, 2),
                ('mute', ctypes.c_uint64, 1),
                ('music', ctypes.c_uint64, 4),                
                ('start', ctypes.c_uint64, 1),
                ('repeat', ctypes.c_uint64, 1),
                ('pad2', ctypes.c_uint64, 2),
                ('volume', ctypes.c_uint64, 4),
                ('pad3', ctypes.c_uint64, 3),
                ('eob', ctypes.c_uint64, 16)]

    def __init__(self, value=0):
        self._eob = 0xffff
        self._off = 1
#        self.value = value
    
    def as_dict(self):
        ret = {}
        for name, *_ in self._fields_:
            if 'pad' in name:
                continue
            name = name.replace('_', '')
            v = getattr(self, name, None)
            ret.setdefault(name, v)
        return ret

    @property
    def width(self):
        try:
            return self._width
        except AttributeError:
            pass
        self._width = sum(b for n,t,b in self._fields_)
        return self._width

    @property
    def value(self):
        r = 0
        shift = self.width
        for name, ctype, bits in self._fields_:
            shift -= bits
            r |= getattr(self, name) << shift
        return r
    
    @value.setter
    def value(self, newValue):

        shift = self.width
        for name, ctype, bits in self._fields_:
            pass
        raise NotImplementedError('value.setter')
    
class BlyncLight(BlyncLightStatus):
    '''
    '''
    @classmethod
    def available_lights(cls):
        '''
        '''
        return [cls.from_dict(d) for d in hid_enumerate(vendor_id=0x2c0d)]

    @classmethod
    def first_light(cls):
        '''
        '''
        try:
            return cls.available_lights()[0]
        except IndexError:
            raise Exception('no blynclights found')

    @classmethod
    def from_dict(cls, device):
        '''
        '''
        return cls(vendor_id=device['vendor_id'],
                   product_id=device['product_id'])

    def __init__(self, vendor_id, product_id, value=None, immediate=True):
        super().__init__(value)
        self._handle = hid_open(vendor_id, product_id)
        self.immediate = immediate

    def __del__(self):
        '''
        '''
        hid_close(self._handle)

    def __repr__(self):
        '''
        '''
        return ''.join([f'{self.__class__.__name__}(',
                        'vendor_id={vendor_id},',
                        'product_id={product_id})'])

    def __str__(self):
        
        return '\n'.join(f'{k:10s}: {v:X}' for k,v in self.as_dict().items())

    @property
    def on(self):
        return 0 if self.off else 1

    @on.setter
    def on(self, newValue):
        self.off = 0 if newValue else 1

    @property
    def bright(self):
        return 0 if self.dim else 1

    @bright.setter
    def bright(self, newValue):
        self.dim = 0 if newValue else 1

    @property
    def color(self, newValue):

        return (self.red, self.blue, self.green)

    @color.setter
    def color(self, newValue):
        try:
            r = (newValue >> 16) & 0x00ff
            b = (newValue >>  8) & 0x00ff
            g = newValue & 0x00ff
            self.red, self.blue, self.green = r,g,b
            return
        except TypeError:
            pass
        self.red, self.blue, self.green = newValue

    def __setattr__(self, name, value):
        '''
        '''
        super().__setattr__(name, value)
        if name in [n for n,c,b in self._fields_] and self.immediate:
            self.update_device()

    def update_device(self):
        '''
        '''
        offset = 7
        return hid_write(self._handle,
                         ctypes.byref(self, offset),
                         ctypes.sizeof(self) - offset)

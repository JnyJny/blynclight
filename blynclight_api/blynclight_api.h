/* blynclight_api.h 
 */
#ifndef BLYNCLIGHT_API_H
#define BLYNCLIGHT_API_H

#define INVALID_DEVICE_TYPE 0

#ifdef __linux
#include "constants.h"
#include "hidapi.h"
#include "embravaapi.h"
#define MAXIMUM_DEVICES MAX_DEVICES_SUPPORTED
struct DeviceInfo
{
  unsigned char byDeviceType;
} asDeviceInfo[MAXIMUM_DEVICES];

#define RETVAL(V) V
#define TurnOffLight ResetLight
#define ReleaseDevices(X) CloseDevices(X)
#define UNIQUE_ID(NDX,UID) UID = GetDeviceUniqueId(NDX) 
#define DEVINFO_ARRAY aosDeviceInfo
#endif	/* __linux */

#ifdef __APPLE__
typedef unsigned char Byte;
typedef unsigned char byte;
#include "Constants.h"
#include "blynclightcontrol.h"
#define RETVAL(V) ((V)==0)?1:0
#define ReleaseDevices(X) ReleaseDevices()
#define InitBlyncDevices(IPTR, ARRAY) FindDevices(IPTR)
#define UNIQUE_ID(NDX,UID) GetDeviceUniqueId(NDX,&(UID)) 
#define DEVINFO_ARRAY asDeviceInfo
#endif	/* __APPLE__ */

int  init_blynclights(void);
void fini_blynclights(void);
int  refresh_blynclights(void);

unsigned int unique_device_id(byte index);

byte device_type(byte index);

int  light_on(byte index, byte r, byte g, byte b);
int  light_off(byte index);

int  bright(byte index, byte mode);

int  flash(byte index, byte mode);
int  flash_speed(byte index, byte speed);

int  music(byte index, byte mode);
int  music_repeat(byte index, byte mode);
int  music_volume(byte index, byte volume);
int  music_select(byte index, byte music);

int  mute(byte index, byte mode);

#endif	/* BLYNCLIGHT_API_H */

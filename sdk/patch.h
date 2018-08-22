#ifndef PATCH_H
#define PATCH_H

#ifdef __linux
#include "constants.h"
#include "hidapi.h"
#include "embravaapi.h"
#define MAXDEV MAX_DEVICES_SUPPORTED
struct DeviceInfo
{
  unsigned char byDeviceType;
} asDeviceInfo[MAXDEV];
#endif

#ifdef __APPLE__
typedef unsigned char Byte;
typedef unsigned char byte;
#include "Constants.h"
#include "blynclightcontrol.h"
#define MAXDEV MAXIMUM_DEVICES
#endif

int  init_blynclights(void);
void fini_blynclights(int ndevices);

unsigned int unique_device_id(byte devIndex);

int  red_on(byte index);
int  green_on(byte index);
int  blue_on(byte index);
int  cyan_on(byte index);
int  magenta_on(byte index);
int  yellow_on(byte index);
int  white_on(byte index);
int  orange_on(byte index);

int  rgb_on(byte index, byte r, byte g, byte b);

int  light_off(byte index);

int  flash_on(byte index);
int  flash_off(byte index);
int  flash_speed(byte index, byte speed);
     
int  music_select(byte index, byte music);
int  music_play(byte index);
int  music_stop(byte index);
int  music_repeat_on(byte index);
int  music_repeat_off(byte index);

int  mute_on(byte index);
int  mute_off(byte index);
int  music_volume(byte index, byte volume);

int  dim(byte index);
int  bright(byte index);

#endif	/* PATCH_H */

#include <stdio.h>

#ifdef __APPLE__
#include "Constants.h"
#include "blynclightcontrol.h"

int init_blynclights(void)
{
  int ndev = 0;
  
  if (FindDevices(&ndev) != 1)
    return -1;
  
  return ndev;
}


void fini_blynclights(int ndev)
{
  ReleaseDevices();
}


int ResetLight(unsigned char devIndex)
{
  return TurnOffLight(devIndex);
}


unsigned int unique_device_id(unsigned char devIndex)
{
  unsigned int uId;

  GetDeviceUniqueId(devIndex, &uId);

  return uId;
}

#endif


#ifdef __linux

#include "Constants.h"
#include "embravaapi.h"

struct DeviceInfo
{
  unsigned char byDeviceType;
};

// Linux has a 10 device limit, so mirror that here
// in the asDeviceInfo array even though it's defined
// to be 32 in the Mac SDK. :shrug:

extern struct DeviceInfo asDeviceInfo[10];

int init_blynclights(void)
{
  int ndev = 0;
  int i;
  
  InitBlyncDevices(&ndev, aosDeviceInfo);

  for(i=0; i<ndev; i++) {
    asDeviceInfo[i].byDeviceType = aosDeviceInfo[i].byDeviceType;
  }
  
  return ndev;
}

void fini_blynclights(int ndev)
{
  CloseDevices(ndev);
}

unsigned int unique_device_id(unsigned char devIndex)
{
  return GetDeviceUniqueId(devIndex);
}

#endif

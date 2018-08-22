#include <stdio.h>

#include "patch.h"

int MAXDEV = MAXIMUM_DEVICES;

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


unsigned int unique_device_id(unsigned char devIndex)
{
  unsigned int uId;

  GetDeviceUniqueId(devIndex, &uId);

  return uId;
}


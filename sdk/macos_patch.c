#include <stdio.h>

#include "patch.h"

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

int red_on(byte index)
{
  return TurnOnRedLight(index);
}

int green_on(byte index)
{
  return TurnOnGreenLight(index);
}

int blue_on(byte index)
{
  return TurnOnBlueLight(index);
}

int cyan_on(byte index)
{
  return TurnOnCyanLight(index);
}

int magenta_on(byte index)
{
  return TurnOnMagentaLight(index);
}

int yellow_on(byte index)
{
  return TurnOnYellowLight(index);
}

int white_on(byte index)
{
  return TurnOnWhiteLight(index);
}

int orange_on(byte index)
{
  return TurnOnOrangeLight(index);
}

int rgb_on(byte index, byte r, byte g, byte b)
{
  return TurnOnRGBLights(index, r, g, b);
}

int light_off(byte index)
{
  return TurnOffLight(index);
}
     
int flash_on(byte index)
{
  return StartLightFlash(index);
}

int flash_off(byte index)
{
  return StopLightFlash(index);
}

int flash_speed(byte index, byte speed)
{
  return SelectLightFlashSpeed(index, speed);
}
     
int music_select(byte index, byte music)
{
  return SelectMusicToPlay(index, music);
}

int music_play(byte index)
{
  return StartMusicPlay(index);
}

int music_stop(byte index)
{
  return StopMusicPlay(index);
}

int music_repeat_on(byte index)
{
  return SetMusicRepeat(index);
}

int music_repeat_off(byte index)
{
  return ClearMusicRepeat(index);
}

int mute_on(byte index)
{
  return SetVolumeMute(index);
}

int mute_off(byte index)
{
  return ClearVolumeMute(index);
}

int music_volume(byte index, byte volume)
{
  return SetMusicVolume(index, volume);
}

int dim(byte index)
{
  return SetLightDim(index);
}

int bright(byte index)
{
  return ClearLightDim(index);
}





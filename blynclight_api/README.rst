BlyncLight API
==============

Overview
--------

API
---
:Interface:
   int  init_blynclights(void);
   
   **Arguments**
     ``void``
   **Returns**
     Returns the number of Blync devices found.
     Device index numbers range from 0 to n-1.
     
   **Notes**

:Interface:
   void fini_blynclights(void);
   
   **Arguments**
      void
   **Returns**
      void

   **Notes**      
   
:Interface:
   int  sync_blynclights(int refresh);
   
   **Arguments**
      - refresh:   0 == do not scan, >1 refresh seconds

   **Returns**
      Returns the number of Blync devices found.

   **Notes**      

:Interface:
   unsigned int unique_device_id(byte index)
   
   **Arguments**:
      - index: blync device index
   **Returns**:
      Returns a zero if the device does not have a unique identifier,
      otherwise returns a unsigned integer.

   **Notes**      

:Interface:
   byte device_type(byte index);
   
   **Arguments**
      - index: blync device index
   **Returns**
      Returns (SUCCESS)?1:0

   **Notes**      

:Interface:
   int  light_on(byte index, byte red, byte green, byte blue);
   
   **Arguments**
      - index: blync device index
      - red: 8-bit red color
      - green: 8-bit green color
      - blue: 8-bit green color
   **Returns**
      Returns (SUCCESS)?1:0

   **Notes**      

:Interface:
   int  light_off(byte index);
   
   **Arguments**
      - index : blync device index
   **Returns**
      Returns (SUCCESS)?1:0

   **Notes**      

:Interface:
   int  bright(byte index, byte mode);
   
   **Arguments**
      - index: blync device index
      - mode: 1 on, 0 off
   **Returns**
      Returns (SUCCESS)?1:0

   **Notes**      

:Interface:
   int  flash(byte index, byte mode);
   
   **Arguments**
      - index: blync device index
      - mode: 1 on, 0 off
   **Returns**
      Returns (SUCCESS)?1:0
   **Notes**
   
:Interface:
   int  flash_speed(byte index, byte speed);
   
   **Arguments**
      - index: blync device index
      - speed: 0=Off, 1=Low, 2=Medium, 3=High
   **Returns**
      Returns (SUCCESS)?1:0
   **Notes**
   
:Interface:
   int  music(byte index, byte mode);
   
   **Arguments**
      - index: blync device index
      - mode: 1 play, 0 stop
   **Returns**
      Returns (SUCCESS)?1:0
   **Notes**
   
:Interface:
   int  music_repeat(byte index, byte mode);
   
   **Arguments**
      - index: blync device index
      - mode: 1 on, 0 off
   **Returns**
      Returns (SUCCESS)?1:0
   **Notes**
   
:Interface:
   int  music_volume(byte index, byte volume);
   
   **Arguments**
      - index: blync device index
      - volume:  
   **Returns**
      Returns (SUCCESS)?1:0
   **Notes**
   
:Interface:
   int  music_select(byte index, byte music);
   
   **Arguments**
      - index: blync device index
      - music: 
   **Returns**
      Returns (SUCCESS)?1:0
   **Notes**
   
:Interface:
   int  mute(byte index, byte mode);
   
   **Arguments**
      - index: blync device index
      - mode: 
   **Returns**
      Returns (SUCCESS)?1:0
   **Notes**


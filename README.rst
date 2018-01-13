Embrava BlyncLight
==================

|pypi| |license| |python|

**blynclight** is a Python package that provides python bindings for the
`Embrava`_ BlyncLight family of products. These bindings have been tested on MacOS and Linux.

Embrava distributes a Software Development Kit (sdk) for Windows, MacOS and Linux that developers must first `request`_ access to. The MacOS and Linux SDKs provide access to BlyncLight devices via a static lirary archive.  Developers then link their applications against the static library. Unfortunately, Python cannot access static library archives via the the ctypes module. Fortunately, it is relatively easy to un package a static library archive into object files and construct a dynamic or shared object.

It is my hope that at some point in the future I can distribute either the URLs or the dynamic libraries directly.



TL;DR
-----

1. `Register`_ with Embrava and receive SDK URLs for your operating system.
2. git clone https://github.com/JnyJny/blynclight.git
3. cd blynclight/sdk && make URL=PLATFORM_URL install
4. cd .. ; pip install -e .


Uninstall with pip:

.. code:: bash

	  $ pip uninstall blynclight

Usage
-----

Once installed, the BlyncLight is yours to command!

.. code:: python

	#from blynclight import BlyncLightControl
	
	lights = BlyncLightControl.availableLights()
	
	light = BlyncLightControl.getLight(lights[0])
	
	red = (255, 0, 0)
	green = (0, 255, 0)
	blue = (0, 0, 255)
	light.color = green
	light.on()
	light.flash = True
	light.color = red
	light.flash = False
	light.cycle(colors=[red, blue], repeat=10)
	light.red = 127
	light.green = 255
	light.dim = True
	light.off()
	
More examples can be found in the contrib directory.



.. |pypi| image:: https://img.shields.io/pypi/v/blynclight.svg?style=flat-square&label=version
    :target: https://pypi.org/pypi/blynclight
    :alt: Latest version released on PyPi

.. |python| image:: https://img.shields.io/pypi/pyversions/blynclight.svg?style=flat-square
   :target: https://pypi.org/project/blynclight/
   :alt: Python Versions	  

.. |license| image:: https://img.shields.io/badge/license-apache-blue.svg?style=flat-square
    :target: https://github.com/erikoshaughnessy/blynclight/blob/master/LICENSE
    :alt: Apache license version 2.0  

.. _Embrava: https://embrava.com
.. _register: https://embrava.com/pages/embrava-software-sdk
.. _request:  https://embrava.com/pages/embrava-software-sdk



Embrava BlyncLight
==================

|pypi| |license| |python|

**blynclight** is a Python 3 package that provides bindings for the
`Embrava`_ BlyncLight family of products. These bindings have been
tested on MacOS and Linux using Embrava models V30, and BLYNCUSB40S-181
USB connected lights.


Install
-------

0. Install `hidapi`_ for your platform:

.. code:: bash

          (rpm Linux distros)# yum install XXXX
          (apt Linux distros)# apt-get install XXXX
          (macOS using brew) $ brew install hidapi

1. pip

.. code:: bash

	  $ python3 -m pip install blynclight
	  $ python3 -m pip install git+https://github.com/JnyJny/blynclight.git

2. Install the Cloned Repository

.. code:: bash

	  $ git clone https://github.com/JnyJny/blynclight.git
	  $ cd blynclight
	  $ python3 -m pip install .
	  


Development
-----------

.. code:: bash

	  $ pip install poetry
	  $ git clone https://github.com/JnyJny/blynclight.git
	  $ cd blynclight
	  $ poetry shell
	  $ ..
	  

Uninstall
---------

.. code:: bash

	  $ python3 -m pip uninstall blynclight



Usage
-----

Once installed, the BlyncLight is yours to command!

.. code:: python

	from blynclight import BlyncLight

	light = BlyncLight.get_light()

	red, blue, green = (255, 0, 0), (0, 255, 0), (0, 0, 255)

	light.color = green           # the light is off and green
	light.on = True               # the light is on and green
	light.flash = True            # the light is on, flashing and green
	light.color = red             # the light is on, flashing and red
	light.flash = False           # the light is on and red
	light.bright = False          # the light is on, dim and red
	light.color = blue            # the light is on, dim and blue
	light.bright = True           # the light is on and blue
	light.on = False              # the light is off and blue


Several command line interfaces are provided when blynclight is installed:

- blync
    Provides command-line access to all light attributes.

- fli
    Flashes the light.. impressively.

- rainbow
    Smoothly transitions the color of the light in a rainbow pattern.

- throbber
    Menacingly ramps the color intensity and then recedes. Over and over again.

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

.. _hidapi: https://github.com/signal11/hidapi

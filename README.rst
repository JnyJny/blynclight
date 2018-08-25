Embrava BlyncLight
==================

|pypi| |license| |python|

**blynclight** is a Python package that provides python bindings for
the `Embrava`_ BlyncLight family of products. These bindings have been
tested on MacOS and Linux using an Embrava V30 USB connected light.


Install
-------

1. pip

.. code:: bash

	  $ pip install blynclight

2. Clone the repo

.. code:: bash

	  $ git clone https://github.com/JnyJny/blynclight.git
	  $ cd blynclight; pip install -e .

Usage
-----

Once installed, the BlyncLight is yours to command!

.. code:: python

	from blynclight import BlyncLight_API

	light = BlyncLight_API.first_light()

	red, green, blue = (255, 0, 0), (0, 255, 0), (0, 0, 255)
	
	light.color = green           # the light is off and green
	light.on = True               # the light is on and green
	light.flash = True            # the light is on, flashing and green
	light.color = red             # the light is on, flashing and red
	light.flash = False           # the light is on and red
	light.bright = False          # the light is on, dim and red
	light.color = blue            # the light is on, dim and blue
	light.bright = True           # the light is on and blue
	light.on = False              # the light is off and blue
	
More examples can be found in the contrib directory of the git repo.


Build
-----
Embrava distributes a Software Development Kit (SDK) for Windows,
MacOS and Linux that developers must first `request`_ access to. The
MacOS and Linux SDKs provide access to BlyncLight devices via a static
library archive.  Developers then link their applications against the
static library. Unfortunately, Python cannot access static library
archives via the the ctypes module. Fortunately, it is relatively easy
to unpackage a static library archive into object files and construct
a dynamic or shared object. Provided of course that the archived
objects are suitable for linking (compiled as position independent
code and the right word length as the target python).


1. `Register`_ with Embrava and receive SDK URLs for your operating system.
   
2. Clone the repo

.. code:: bash

          $ git clone https://github.com/JnyJny/blynclight.git

	  
3. Build and install the shared object from the SDK

.. code:: bash

          $ cd blynclight/blynclight_api && make URL=PLATFORM_URL install

	  
4. Install the package

.. code:: bash

          $ cd .. ; pip install -e .


Uninstall with pip:

.. code:: bash

	  $ pip uninstall blynclight


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



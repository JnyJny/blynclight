#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages

here = Path(__file__).absolute().parent

README = here.joinpath('README.rst').read_text()

version = here.joinpath('VERSION').read_text().strip()

# this module can be zip-safe if the zipimporter implements
# iter_modules or if pkgutil.iter_importer_modules has registered a
# dispatch for the zipimporter.
try:
    import pkgutil
    import zipimport
    zip_safe = hasattr(zipimport.zipimporter, "iter_modules") or \
        zipimport.zipimporter in pkgutil.iter_importer_modules.registry.keys()
except (ImportError, AttributeError):
    zip_safe = False

setup(
    name='blynclight',
    version=version,
    description="Python bindings to control Embrava BlyncLight devices.",
    long_description=README,
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License'
    ],
    keywords='blynclight usb macos linux',
    author="Erik O\'Shaughnessy",
    author_email='erik.oshaughnessy@gmail.com',
    url='https://github.com/jnyjny/blynclight',
    license='Apache License, Version 2.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    platforms=['any'],
    test_suite='pytest',
    zip_safe=zip_safe,
    setup_requires=[
        'pytest-runner',
        'readme-renderer',
        'twine'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-flakes',
        'pytest-pep8',
    ],
    install_requires=[
        'requests',
    ],
)

#!/usr/bin/env python3

#
# ColorPro - Color Compution Helper
# Copyright 2015 Sebastian Software GmbH, Germany
#

import sys

if sys.version < "3.3":
  print("ColorPro requires Python 3.3 or higher")
  sys.exit(1)

# Prefer setuptools (aka distribute) over distutils
# - Distutils comes with Python3 but is not capable of installing requires, extras, etc.
# - Distribute is a fork of the Setuptools project (http://packages.python.org/distribute/)
try:
  from setuptools import setup
  uses = "distribute"
except ImportError:
  print("ColorPro prefers distribute over distutils for installing dependencies!")
  from distutils.core import setup
  uses = "distutils"

# Import ColorPro for version info etc.
import colorpro

# Run setup
setup(
  name = 'colorpro',
  version = colorpro.__version__,

  author = 'Sebastian Software',
  author_email = 'team@sebastian-software.de',

  maintainer = 'Sebastian Software',
  maintainer_email = 'team@sebastian-software.de',

  url = 'http://github.com/sebastian-software/colorpro',
  download_url = "http://pypi.python.org/packages/source/c/colorpro/colorpro-%s.zip" % jasy.__version__,

  license = "MIT",
  platforms = 'any',

  description = "Python based optionated color transformation tool.",

  # Via: http://pypi.python.org/pypi?%3Aaction=list_classifiers
  classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Software Development"
  ],

  packages = [
    "colorpro"
  ],

  data_files = [
    ("colorpro", [
      "license.md",
      "readme.md",
      "requirements.txt"
     ]
    )
  ],

  scripts = [ "bin/colorpro" ]

  install_requires = [
    "numpy>=1.9",
    "scipy>=0.15",
    "colour-science>=0.3"
  ]
)

"""
    File: setup.py - Builds isacpp and links with Python using SWIG
    Author : Alberto Lorenzo
"""

from distutils.core import setup, Extension
import numpy

basename = 'isacpp'
version = '0.1.1'

extension = Extension('_' + basename,
                      sources=[basename + '_wrap.cxx', 
                               basename +'.cpp'],
                      include_dirs=[numpy.get_include()],)

setup(name = basename,
      version = version,
      author      = 'Alberto Lorenzo',
      description = """ISA Model implemented in C++""",
      ext_modules = [extension],
      py_modules = [basename],)

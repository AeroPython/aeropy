from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
import os

import numpy

version = '1.5.1'
base_name = 'isa'
include_path = \
    os.path.join(os.path.abspath(__file__)
                 [:-1 - len(os.path.basename(__file__))], 'include')

copt = {'msvc': ['/openmp', '/Ox'],
        'mingw32': ['-fopenmp', '-O3'],
        'mingw64': ['-fopenmp', '-O3'],
        'cygwin': ['-fopenmp', '-O3'],
        'unix': ['-fopenmp', '-O3']}
lopt = {'mingw32': ['-lgomp'],
        'mingw64': ['-lgomp'],
        'cygwin': ['-lgomp'],
        'unix': ['-lgomp']}


class build_ext_subclass(build_ext):

    def build_extensions(self):
        c = self.compiler.compiler_type
        if c in copt:
            for e in self.extensions:
                e.extra_compile_args = copt[c]
        if c in lopt:
            for e in self.extensions:
                e.extra_link_args = lopt[c]
        build_ext.build_extensions(self)

ext_name = 'isacpp'
ext_folder = os.path.join(base_name, ext_name)
extension = Extension(base_name + '.' + ext_name + '._' + ext_name,
                      language='c++',
                      sources=[os.path.join(ext_folder, ext_name + '.i'),
                               os.path.join(ext_folder, ext_name + '.cpp'),
                               os.path.join(ext_folder, 'cstmath.cpp')],
                      swig_opts=['-c++', '-py3', '-I' + include_path],
                      include_dirs=[numpy.get_include()],)

setup(name=base_name,
      version=version,
      author='Alberto Lorenzo',
      description='ISA Model computed in C++',
      ext_modules=[extension],
      cmdclass={'build_ext': build_ext_subclass},
      packages=[base_name, base_name + '.' + ext_name],)

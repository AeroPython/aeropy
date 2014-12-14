from distutils.core import setup, Extension
import numpy

version = '1.1.1'

base_name = 'isa'

ext_name = 'isacpp'
ext_folder = 'isa/isacpp/'
extension = Extension(base_name + '.' + ext_name + '._' + ext_name,
                      sources=[ext_folder + ext_name + '_wrap.cxx', 
                               ext_folder + ext_name + '.cpp'],
                      include_dirs=[numpy.get_include()],)

setup(name = base_name,
      version = version,
      author      = 'Alberto Lorenzo',
      description = 'ISA Model with calculations implemented in C++',
      ext_modules = [extension],
      packages = [base_name, base_name + '.' + ext_name],)

from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
           "tokenization",                                # the extension name
           sources=["tokenization.pyx", "charmap.cpp"], # the Cython source and
                                                  # additional C++ source files
           language="c++",                        # generate and compile C++ code
           extra_compile_args=['-O2', '-mtune=native']
      )))

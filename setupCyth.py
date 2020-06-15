from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='Hello world app',
    ext_modules=cythonize("weball.pyx"),
    zip_safe=False,
    include_dirs=[numpy.get_include()],
)

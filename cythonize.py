'''cythonize'''

from distutils.core import setup
from Cython.Build import cythonize


setup(
    name = 'Pretty Path Class',
    ext_modules=cythonize("cprettypath1.pyx")
    )

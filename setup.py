from distutils.core import setup,Extension
setup(name="vec2d",version="0.1",ext_modules=[Extension("vec2d",["vec2dmodule.c"])])

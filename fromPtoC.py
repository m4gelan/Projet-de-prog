from distutils.core import setup, Extension

projetModule = Extension('fromCtoPy', sources = ['fromCtoPy.c'], libraries = [])

setup(name = 'simulation de la comete',
      version = '1.0',
      description = 'Module du projet de simulation.',
      ext_modules = [projetModule]);

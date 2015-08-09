#!/usr/bin/env python
from setuptools import setup, find_packages
import sys
import os

if os.environ.get('USE_PANDOC'):
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')

    pypandoc.convert('man/MANUAL.1.md', 'man', extra_args=['-s'],
                     outputfile='man/thefuck.1')
    data_files = [("share/man/man1/", ["man/thefuck.1"])]
else:
    long_description = ''
    data_files = []

version = sys.version_info[:2]
if version < (2, 7):
    print('thefuck requires Python version 2.7 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)
elif (3, 0) < version < (3, 3):
    print('thefuck requires Python version 3.3 or later' +
          ' ({}.{} detected).'.format(*version))
    sys.exit(-1)

VERSION = '2.6'

install_requires = ['psutil', 'colorama', 'six']
extras_require = {':python_version<"3.4"': ['pathlib']}

setup(name='thefuck',
      version=VERSION,
      description="Magnificent app which corrects your previous console command",
      long_description=long_description,
      author='Vladimir Iakovlev',
      author_email='nvbn.rm@gmail.com',
      url='https://github.com/nvbn/thefuck',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'tests', 'release']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require=extras_require,
      data_files=data_files,
      entry_points={'console_scripts': [
          'thefuck = thefuck.main:main',
          'thefuck-alias = thefuck.main:print_alias']})

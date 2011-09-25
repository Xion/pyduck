#!/usr/bin/env python
'''
Setup script for the pyduck project.

Created on 2011-09-25

@author: xion
'''
from setuptools import setup, find_packages


setup(name = 'pyduck',
      version = '1.0',
      description = 'Utility framework for effective use of duck typing via Go-like interfaces',
      long_description = open("README.markdown").read(),
      author = 'Karol Kuczmarski "Xion"',
      author_email = "karol.kuczmarski@gmail.com",
      url = "http://github.com/Xion/pyduck",
      license = "MIT",
      classifiers = [
                     'Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Information Technology',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.5',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Topic :: Software Development',
                     'Topic :: Software Development :: Libraries',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     ],
      
      packages = find_packages(exclude = ['tests']),
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

install_requires = [
    'numpy',
    'audiotrans'
]

setup(name='audiotrans-transform-istft',
      version='0.1.0.dev2',
      description="""audiotrans transform module to Inverse Short-Time Fourier Transformation (ISTFT)""",  # NOQA
      author='keik',
      author_email='k4t0.kei@gmail.com',
      url='https://github.com/keik/audiotrans-transform-istft',
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Topic :: Multimedia :: Sound/Audio :: Conversion',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ],
      packages=find_packages(),
      install_requires=install_requires)

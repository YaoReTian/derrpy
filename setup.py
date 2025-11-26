#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:17:09 2025

@author: YaoReTian

setup.py
"""

from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

src = ["derrpy.py"]
extensions = cythonize(Extension(
             name="derrpy",
             sources = src
      ))

setup (
       name = "derrpy",
       version = "0.1.0",
       author = "YaoReTian",
       url = "https://github.com/YaoReTian/derrpy",
       packages = find_packages(),
       ext_modules= extensions,
       install_requires=['numpy>=']
)
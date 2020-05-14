#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Distutils setup file for homoeditdistance
"""

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='homoeditdist-pkg-guwekl', 
    version='0.0.1',
    author='Maren Brand, Gunnar W. Klau',
    author_email='gunnar.klau@hhu.de',
    description='An implementation of the homo-edit distance',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AlBi-HHU/homo-edit-distance',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    python_requires='>=3.6',
    install_requires='numpy',
    entry_points={'console_scripts': ['homoeditdistance=homoeditdistance.demonstration:main']},
)

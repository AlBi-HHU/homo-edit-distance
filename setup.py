#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Distutils setup file for homoeditdistance
"""

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='homoeditdistance',
    version='0.0.1',
    author='Maren Brand, Gunnar W. Klau, Philipp Spohr, Nguyen Khoa Tran, Max Jakub Ried',
    author_email='albi-packaging@hhu.de',
    description='An implementation of the homo-edit distance algorithm.',
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
    python_requires='>=3.4',
    install_requires='numpy',
    entry_points={'console_scripts': ['hed=homoeditdistance.demonstration:main']},
)

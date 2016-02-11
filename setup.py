#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'fitsio',
]

test_requirements = [
    'pytest',
    'numpy',
]

setup(
    name='fitsioyielder',
    version='0.0.1',
    description="Package to efficiently read large fits arrays in object by object",
    long_description=readme + '\n\n' + history,
    author="Simon Walker",
    author_email='s.r.walker101@googlemail.com',
    url='https://github.com/mindriot101/fitsioyielder',
    packages=[
        'fitsioyielder',
    ],
    package_dir={'fitsioyielder':
                 'fitsioyielder'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='fitsioyielder',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=['pytest-runner'],
)

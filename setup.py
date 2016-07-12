#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    "pytest", "pytest-cov"
]

setup(
    name='islex',
    version='0.1.1',
    description="Utility classes to support easy loading and manipulation of dictionary-to-pronunciation.",
    long_description=readme + '\n\n' + history,
    author="Jeremy G. Kahn",
    author_email='jeremy@trochee.net',
    url='https://github.com/jkahn/islex',
    packages=[
        'islex',
    ],
    package_dir={'islex':
                 'islex'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='islex',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    setup_requires=['pytest-runner',],
    test_suite='tests',
    tests_require=test_requirements
)

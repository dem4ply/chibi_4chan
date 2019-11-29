#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'chibi_request==0.5', 'babel=2.7.0', 'PTable>=0.9.2' ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Dem4ply",
    author_email='dem4ply@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="api wrapper for 4chan",
    entry_points={
        'console_scripts': [
            'chibi_4chan=chibi_4chan.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chibi_4chan',
    name='chibi_4chan',
    packages=find_packages(include=['chibi_4chan', 'chibi_4chan.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dem4ply/chibi_4chan',
    version='0.5.0',
    zip_safe=False,
)

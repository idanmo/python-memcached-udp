#!/usr/bin/env python

# Copyright 2015 Idan Moyal. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(
    name='python-memcached-udp',
    version='0.1a',
    description='A simple UDP Memcached client written in Python.',
    long_description=open("README.md").read(),
    url='https://github.com/idanmo/python-memcached-udp',
    author='Idan Moyal',
    author_email='idanmo@gmail.com',
    py_modules=["memcached_udp"],
    install_requires=[
        "six==1.10.0",
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)

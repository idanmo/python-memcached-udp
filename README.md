[![Build Status](https://travis-ci.org/idanmo/python-memcached-udp.svg?branch=master)](https://travis-ci.org/idanmo/python-memcached-udp)

# UDP Memcached client for Python
A simple UDP Memcached client implementation written in Python.

Implemented for my own needs, use at your own risk :-)

## Python Compatibility
* >= 2.7 (3 included)

## Supported Operations
* set
* get

## Installation

```
pip install https://github.com/idanmo/python-memcached-udp/archive/master.zip
```

## Usage:

```python
import memcached_udp

client = memcached_udp.Client([('192.168.0.1', 11211), ('192.168.0.5', 11211)])
client.set('key1', 'value1')
r = client.get('key1')
```

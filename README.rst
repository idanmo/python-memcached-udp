
Python Memcached UDP Client
===========================

.. image:: https://img.shields.io/pypi/v/python-memcached-udp.svg
    :target: https://pypi.python.org/pypi/python-memcached-udp

.. image:: https://travis-ci.org/idanmo/python-memcached-udp.svg?branch=master
    :target: https://travis-ci.org/idanmo/python-memcached-udp


A simple UDP Memcached client implementation written in Python.

Implemented for my own needs, use at your own risk :-)


Python Compatibility
--------------------
>= 2.7 (3 included)


Supported Operations
--------------------
- set
- get


Installation
------------

.. code-block:: python

    pip install python-memcached-udp


Usage
-----

.. code-block:: python

    import memcached_udp

    client = memcached_udp.Client([('192.168.0.1', 11211), ('192.168.0.5', 11211)])
    client.set('key1', 'value1')
    r = client.get('key1')


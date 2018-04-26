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

import threading
import unittest
import time

import memcached_udp


class MemcachedUDPTest(unittest.TestCase):

    client = None

    def setUp(self):
        self.client = memcached_udp.Client([('127.0.0.1', 11211)], debug=True)

    def test_server_not_responding(self):
        client = memcached_udp.Client([('127.0.0.1', 9999)], debug=True)
        self.assertRaises(
            memcached_udp.Client.MemcachedServerNotRespondingError,
            client.get,
            'abcd')

    def test_set_get(self):
        key = 'key1'
        value = 'value-123456'
        self.client.set(key, value)
        result = self.client.get(key)
        self.assertEqual(value, result)

    def test_get_key_not_found(self):
        self.assertIsNone(self.client.get('not-found'))

    def test_parallel_gets(self):
        err = []
        lock = threading.Lock()

        def set_values(thread_number):
            try:
                for i in range(0, 50):
                    key = '{0}-key-parallel-{1}'.format(thread_number, i)
                    value = '{0}-value-parallel-{1}'.format(thread_number, i)
                    self.client.set(key, value)
                for i in range(0, 50):
                    key = '{0}-key-parallel-{1}'.format(thread_number, i)
                    value = '{0}-value-parallel-{1}'.format(thread_number, i)
                    r = self.client.get(key)
                    if value != r:
                        with lock:
                            err.append('{0} != {1}'.format(value, r))
            except Exception as e:
                with lock:
                    err.append(str(e))

        threads = [threading.Thread(
            target=set_values, args=[x]) for x in range(0, 5)]
        for t in threads:
            t.start()

        done = False
        while not done:
            done = True
            for t in threads:
                if t.is_alive():
                    done = False
                    break
            time.sleep(1)

        if err:
            self.fail(err)

    def test_multi_packet_response(self):
        payload = 'B' * 65400 + 'A'
        client = memcached_udp.Client([('localhost', 11211)])
        client.set('multi-packet-response', payload)
        r = client.get('multi-packet-response')
        self.assertEquals(payload, r)


class MemcachedUDPClusterTest(MemcachedUDPTest):

    def setUp(self):
        self.client = memcached_udp.Client(
            [('127.0.0.1', 11211), ('127.0.0.1', 11212)], debug=True)

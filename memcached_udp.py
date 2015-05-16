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

import socket
import struct
import threading
import time


class Client(object):

    class MemcachedServerNotRespondingError(Exception):
        pass

    def __init__(self, servers, debug=False, response_timeout=10):
        self.servers = servers
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(5)
        self._results_handler_thread = threading.Thread(
            target=self._get_results_handler)
        self._results_handler_thread.setDaemon(True)
        self._results_handler_thread.start()
        self._server_results = {x: {} for x in self.servers}
        self._server_locks = {x: (0, threading.Lock()) for x in self.servers}
        self._response_timeout = response_timeout
        self._debug = debug

    def _get_results_handler(self):
        while True:
            try:
                data, server = self.socket.recvfrom(4096)
                udp_header = struct.unpack('!hhhh', data[:8])
                if self._debug:
                    print(
                        'memcached_udp: results_handler [server]: {0}'.format(
                            server))
                    print('memcached_udp: results_handler [data]: {0}'.format(
                        data))
                    print('memcached_udp: id={0}, packet_number={1}, '
                          'total_packets={2}, misc={3}'.format(*udp_header))
                server_results = self._server_results[server]
                lock = self._server_locks[server][1]
                with lock:
                    request_id = udp_header[0]
                    server_results[request_id] = data[8:]
            except socket.timeout:
                pass

    def _get_udp_header(self, request_id):
        return struct.pack('!hhhh', request_id, 0, 1, 0)

    def _pick_server(self, key):
        return self.servers[hash(key) % len(self.servers)]

    def _get_request_id(self, server):
        lock = self._server_locks[server][1]
        with lock:
            request_id = self._server_locks[server][0]
            next_request_id = request_id + 1 if request_id < 60000 else 0
            server_results = self._server_results[server]
            if request_id in server_results:
                raise RuntimeError(
                    'Request id already exists for server [server={0}, '
                    'request_id={1}]'.format(server, request_id))
            self._server_locks[server] = (next_request_id, lock)
            return request_id

    def _wait_for_result(self, server, request_id):
        server_results = self._server_results[server]
        deadline = time.time() + self._response_timeout
        while request_id not in server_results:
            if time.time() >= deadline:
                raise self.MemcachedServerNotRespondingError(
                    'Memcached server is not responding: {0}'.format(server))
            time.sleep(0.1)
        result = server_results[request_id]
        del server_results[request_id]
        return result

    def set(self, key, value):
        server = self._pick_server(key)
        request_id = self._get_request_id(server)
        cmd = '{0}set {1} 0 0 {2}\r\n{3}\r\n'.format(
            self._get_udp_header(request_id), key, len(value), value)

        self.socket.sendto(cmd, server)

        r = self._wait_for_result(server, request_id)

        if r.split('\r\n')[0] != 'STORED':
            raise RuntimeError(
                'Error storing "{0}" in {1}'.format(key, server))

    def get(self, key):
        server = self._pick_server(key)
        request_id = self._get_request_id(server)
        cmd = '{0}get {1}\r\n'.format(self._get_udp_header(request_id), key)

        self.socket.sendto(cmd, server)

        r = self._wait_for_result(server, request_id)

        if r.startswith('VALUE'):
            arr = r.split('\r\n')
            return '\r\n'.join(arr[1:len(arr)-2])
        return None

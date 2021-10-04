#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    # get host and port of the url you want 
    def get_host_port(self,url):
        block = (urllib.parse.urlparse(url))
        scheme = block.scheme
        port = block.port
        host = block.hostname

        # port 80 for Http or the url already contains host and port
        if scheme == "http" and port == None:
            return host, 80
        else:
            return host, port

    # Constructing GET request to send to server 
    def request_data(self, url, host_name):
        block = (urllib.parse.urlparse(url))
        path = block.path
        if path == "":
            path = "/"
        else:   
            path
        payload = f'GET {path} HTTP/1.1\r\nHost: {host_name}\r\nAccept: */*\r\nConnection: close\r\n\r\n'
        print("payload constructed")
        #send payload
        self.sendall(payload)

    # Constructing POST to the server
    def post_data(self, url, host_name):
        pass

    # creating the connection once we have host and port
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    # get status code
    def get_code(self, data):
        return int(data.split()[1])

    # get headers of response
    def get_headers(self,data):
        return data.split("\r\n\r\n")[0]

    # get body of response
    def get_body(self, data):
        return data.split("\r\n\r\n")[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""

        host_name, client_port = self.get_host_port(url)
        self.connect(host_name, client_port)

        #construct and sent request
        self.request_data(url, host_name)

        # respond from server
        response = self.recvall(self.socket)

        status_code = self.get_code(response)
        headers = self.get_headers(response)
        body = self.get_body(response)

        print(status_code)
        print(headers)
        print(body)
        self.close()
        return HTTPResponse(status_code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        host_name, client_port = self.get_host_port(url)

        '''
        self.connect(host_name, client_port)
        self.post_data(url, host_name)

        # respond from server
        response = self.recvall(self.socket)
        return HTTPResponse(status_code, body)
        '''

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            print("Post")
            return self.POST( url, args )
        else:
            print("Get")
            return self.GET( url, args )
        
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print("Method and URL")
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print("Just Method")
        print(client.command( sys.argv[1] ))

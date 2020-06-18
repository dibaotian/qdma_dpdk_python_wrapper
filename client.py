#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9527        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))

    
    client.sendall(b'Hello, world')
    client.sendall(b'Hello, world')
    client.sendall(b'Hello, world')
    client.sendall(b'Hello, world')

    data = client.recv(1024)

print('Received', repr(data))
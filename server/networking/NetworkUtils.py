import socket
import json
import hashlib
import struct


def recv_all(self):
    """
    Deal with longer data
    """
    b = self.recv(4)
    if len(b) != 4:
        return bytes()
    size = struct.unpack('>i', b)[0]
    b = bytes()
    while len(b) < size:
        b += self.recv(size - len(b))
    return b


socket.socket.recv_all = recv_all


def pack_data(d):
    b = json.dumps(d).encode('utf-8')
    b = struct.pack('>i', len(b)) + b
    return b


def unpack_data(b: bytes):
    d = json.loads(b.decode('utf-8'))
    return d


def encrypt():
    pass


def decrypt():
    pass


def authenticate():
    pass


if __name__ == '__main__':
    pass
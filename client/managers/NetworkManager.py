from typing import *
import socket
import threading
import time
import json
import struct
from networking.NetworkUtils import *
# added something like recv_all() so do not remove it


class NetworkManager(object):
    # TODO: Authentication needed?

    def __init__(self):
        self.connection: socket.socket = None
        self.addr = None
        self.recv_list = []
        self.send_list = []

    def recv_thread(self, s: socket.socket):
        while True:
            try:
                b = s.recv_all()
                if len(b) == 0:
                    time.sleep(0.001)
                    continue
                d = unpack_data(b)
                self.recv_list.append((s.getsockname(), s.getpeername(), tuple(d)))
            except ConnectionError as err:
                self.removePort(s)
                break
            except Exception as err:
                print(err)

    def connect_thread(self, addr: tuple):
        print(addr)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        print(addr, "connected")
        self.connection = s
        self.addr = addr
        t = threading.Thread(target=self.recv_thread, args=(s,))
        t.setDaemon(True)
        t.start()

    def connectPort(self, addr: tuple):
        t = threading.Thread(target=self.connect_thread, args=(addr, ))
        t.setDaemon(True)
        t.start()

    def removePort(self, s: socket.socket):
        s.close()

    def flush(self):
        self.recv_list.clear()
        self.send_list.clear()

    def dataRead(self, flush: bool = False) -> tuple:
        """
        Args:
            flush: Set to False if you need it after reading
        Returns: tuple of (event_type, ...)
        """
        ret = tuple(self.recv_list)
        if flush:
            self.recv_list.clear()
        return ret

    def dataWrite(self, d) -> None:
        self.send_list.append(d)

    def update(self):
        if self.connection is not None:
            for d in self.send_list:
                self.connection.send(pack_data(d))
            self.send_list.clear()


if __name__ == '__main__':
    nmsl = NetworkManager()
    nmsl.connectPort(("127.0.0.1", 4119))
    while True:
        print(nmsl.dataRead())
        nmsl.dataWrite({"piece of shit": True})
        nmsl.update()
        nmsl.flush()
        time.sleep(1)

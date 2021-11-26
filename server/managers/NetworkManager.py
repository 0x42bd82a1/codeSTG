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
        self.connection_count = 0
        self.connection_pool = []  # stores [laddr]
        self.sock_to_peer = {}     # stores {laddr: [raddr]}
        self.recv_list = []
        self.send_all_list = []
        self.send_list = []

    def recv_thread(self, s: socket.socket):
        while True:
            try:
                b = s.recv_all()
                if len(b) == 0:
                    time.sleep(0.008)
                    continue
                d = unpack_data(b)
                self.recv_list.append((s.getsockname(), s.getpeername(), tuple(d)))
            except ConnectionError as err:
                self.removePort(s)
                break
            except Exception as err:
                print(err)

    def bind_thread(self, s: socket.socket):
        while True:
            conn, addr = s.accept()
            print(addr, "connected")
            self.connection_pool.append(conn)
            self.sock_to_peer[s.getsockname()].append(conn)
            t = threading.Thread(target=self.recv_thread, args=(conn,))
            t.setDaemon(True)
            t.start()
            self.connection_count += 1

    def bindPort(self, addr: Tuple[str, int]):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(16)
        self.sock_to_peer[addr] = []
        t = threading.Thread(target=self.bind_thread, args=(s,))
        t.setDaemon(True)
        t.start()

    def removePort(self, s: socket.socket) -> None:
        if s in self.connection_pool:
            print(s.getpeername(), "disconnecting")
            self.connection_pool.remove(s)
            self.sock_to_peer[s.getsockname()].remove(s)
            s.close()
            self.connection_count -= 1

    def flush(self):
        self.recv_list.clear()
        self.send_list.clear()
        self.send_all_list.clear()

    def dataRead(self, flush: bool = False) -> tuple:
        """
        Args:
            flush: Set to False if you need it after reading
        Returns: (laddr, raddr, others...)
        """
        ret = tuple(self.recv_list)
        if flush:
            self.recv_list.clear()
        return ret

    def dataWrite(self, d, host: str = None, port: int = None) -> None:
        """
        Args:
            d: data to send
            host: Send data to all hosts connected when set to None
            port: Send data to all hosts connected when set to None
        """
        if host is None or port is None:
            self.send_all_list.append(d)
        else:
            self.send_list.append(((host, port), d))

    def update(self):
        for s in self.connection_pool:
            for d in self.send_all_list:
                try:
                    s.send(pack_data(d))
                except ConnectionError as err:
                    # self.removePort(s)
                    pass
        for sd in self.send_list:
            if sd[0] in self.sock_to_peer:
                for s in self.sock_to_peer[sd[0]]:
                    try:
                        s.send(pack_data(sd[1]))
                    except ConnectionError as err:
                        # self.removePort(s)
                        pass
                    except Exception as err:
                        print(err)
        self.send_all_list.clear()
        self.send_list.clear()
        pass

    def exit(self):
        for s in self.connection_pool:
            s.close()


if __name__ == '__main__':
    nmsl = NetworkManager()
    nmsl.bindPort(("127.0.0.1", 4119))
    while True:
        print(nmsl.dataRead())
        nmsl.dataWrite({"piece of shit": True})
        nmsl.dataWrite({"str": "specific port"}, ('127.0.0.1', 4119))
        nmsl.update()
        nmsl.flush()
        time.sleep(1)

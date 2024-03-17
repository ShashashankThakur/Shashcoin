# NOT USED (YET)

import socket


class Network:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self, peer_host, peer_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((peer_host, peer_port))
            return sock
        except ConnectionRefusedError:
            print(f"Connection to {peer_host}:{peer_port} refused")
            return None

    def disconnect(self, sock):
        sock.close()


if __name__ == "__main__":
    network = Network('localhost', 9999)

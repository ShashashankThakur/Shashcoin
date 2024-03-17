import socket
import threading

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.connections = []

    def start(self):
        self.sock.listen(5)
        print(f"Node listening at {self.host}:{self.port}")
        while True:
            client, address = self.sock.accept()
            print(f"Connection established with {address}")
            self.connections.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(1024)
                if data:
                    print(f"Received: {data.decode()}")
            except ConnectionResetError:
                print("Connection closed by peer")
                self.connections.remove(client)
                client.close()
                break

    def send_message(self, message):
        for conn in self.connections:
            conn.sendall(message.encode())

    def connect_to_network(self, other_nodes):
        for node in other_nodes:
            if node != (self.host, self.port):  # Avoid connecting to itself
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    sock.connect(node)
                    self.connections.append(sock)
                    print(f"Connected to {node}")
                except ConnectionRefusedError:
                    print(f"Connection to {node} refused")

    def close(self):
        for conn in self.connections:
            conn.close()
        self.sock.close()

if __name__ == "__main__":
    node = Node('localhost', 9999)
    node.start()

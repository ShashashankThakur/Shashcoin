import socket
import threading
import pickle
from src.blockchain.blockchain import Blockchain
from src.mining.proof_of_work import ProofOfWork


class Node:
    def __init__(self, host, port, other_nodes=[]):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.connections = []
        self.blockchain = Blockchain()
        self.connect_to_network(other_nodes)

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
                data = client.recv(4096)
                if data:
                    message = pickle.loads(data)
                    print(f"Received: {message}")
                    if 'block' in message:
                        new_block = message['block']
                        if ProofOfWork.is_valid_hash(new_block):
                            self.blockchain.add_block(new_block)
                            print("Added block to blockchain")
                            self.broadcast_block(new_block)
                        else:
                            print("Received invalid block")
            except ConnectionResetError:
                print("Connection closed by peer")
                self.connections.remove(client)
                client.close()
                break

    def send_message(self, message):
        serialized_message = pickle.dumps(message)
        for conn in self.connections:
            conn.sendall(serialized_message)

    def connect_to_network(self, other_nodes):
        for node in other_nodes:
            if node != (self.host, self.port):  # Avoid connecting to itself
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    sock.connect(node)
                    self.connections.append(sock)
                    print(f"Connected to {node}")
                    # Share blockchain with connected node
                    self.send_message({'blockchain': self.blockchain.chain})
                except ConnectionRefusedError:
                    print(f"Connection to {node} refused")

    def broadcast_block(self, new_block):
        message = {'block': new_block}
        self.send_message(message)

    def close(self):
        for conn in self.connections:
            conn.close()
        self.sock.close()


if __name__ == "__main__":
    node = Node('localhost', 9999)
    node.start()

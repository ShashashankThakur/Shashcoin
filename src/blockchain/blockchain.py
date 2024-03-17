import hashlib
import json
from time import time
import socket
import threading
import pickle

# Define constants
MINING_DIFFICULTY = 4
NODE_PORT = 8888
BUFFER_SIZE = 4096


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash_block(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
        self.peers = []

    def create_genesis_block(self):
        """
        Genesis block
        """
        genesis_block = Block(index=0,
                              timestamp=time(),
                              data="Genesis Block",
                              previous_hash="0")
        self.chain.append(genesis_block)

    def add_block(self, block):
        block.previous_hash = self.chain[-1].hash_block()
        self.chain.append(block)

    def mine_block(self, data):
        """
        Mines a new block with the given data
        """
        index = len(self.chain)
        timestamp = time()
        previous_hash = self.chain[-1].hash_block()
        nonce = 0
        new_block = Block(index, timestamp, data, previous_hash, nonce)

        # Proof of Work
        while not self.valid_proof(new_block):
            new_block.nonce += 1

        self.add_block(new_block)

    def valid_proof(self, block):
        """
        Validates the proof of work for a given block
        """
        guess = json.dumps(block.__dict__, sort_keys=True).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:MINING_DIFFICULTY] == "0" * MINING_DIFFICULTY

    def broadcast_block(self, block):
        """
        Broadcasts a newly mined block to all connected peers
        """
        for peer in self.peers:
            self.send_block(peer, block)

    def send_block(self, peer, block):
        """
        Sends a block to a specified peer
        """
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect(peer)
        peer_socket.sendall(pickle.dumps(block))
        peer_socket.close()

    def receive_blocks(self, conn, addr):
        """
        Receives blocks from a connected peer
        """
        data = b""
        while True:
            received_data = conn.recv(BUFFER_SIZE)
            if not received_data:
                break
            data += received_data
        block = pickle.loads(data)
        self.add_block(block)

    def start_server(self):
        """
        Starts the server to listen for incoming connections
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", NODE_PORT))
        server_socket.listen()
        print(f"Server listening on port {NODE_PORT}...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected to {addr}")
            threading.Thread(target=self.receive_blocks, args=(conn, addr)).start()


# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    # Start server in a separate thread
    threading.Thread(target=blockchain.start_server).start()

    # Mine some blocks
    blockchain.mine_block("Transaction Data 1")
    blockchain.mine_block("Transaction Data 2")

    # Broadcast new blocks to peers
    for block in blockchain.chain[1:]:
        blockchain.broadcast_block(block)

    # Display the blockchain
    for block in blockchain.chain:
        print("Index:", block.index)
        print("Timestamp:", block.timestamp)
        print("Data:", block.data)
        print("Previous Hash:", block.previous_hash)
        print("Nonce:", block.nonce)
        print("Hash:", block.hash_block())
        print("----------------------------------")

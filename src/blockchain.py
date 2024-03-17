import hashlib
import json
from time import time


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
        return guess_hash[:4] == "0000"


# Example usage
blockchain = Blockchain()

# Mine some blocks
blockchain.mine_block("Transaction Data 1")
blockchain.mine_block("Transaction Data 2")

# Display the blockchain
for block in blockchain.chain:
    print("Index:", block.index)
    print("Timestamp:", block.timestamp)
    print("Data:", block.data)
    print("Previous Hash:", block.previous_hash)
    print("Nonce:", block.nonce)
    print("Hash:", block.hash_block())
    print("----------------------------------")

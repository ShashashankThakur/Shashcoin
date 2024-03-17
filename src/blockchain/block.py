import hashlib
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = (str(self.index) + str(self.timestamp) + str(self.data) +
                        str(self.previous_hash) + str(self.nonce))
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __str__(self):
        return (
            f"Index: {self.index}\n"
            f"Timestamp: {self.timestamp}\n"
            f"Data: {self.data}\n"
            f"Previous Hash: {self.previous_hash}\n"
            f"Nonce: {self.nonce}\n"
            f"Hash: {self.hash}\n"
        )


if __name__ == "__main__":
    block = Block(0, time.time(), "Genesis Block", "0")
    difficulty = 4
    block.mine_block(difficulty)
    print(block)

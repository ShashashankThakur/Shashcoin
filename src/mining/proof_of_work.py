import hashlib


class ProofOfWork:
    @staticmethod
    def calculate_hash(block):
        """
        Calculate the hash of a block
        Same as function defined in block.py
        """
        block_string = (str(block.index) + str(block.timestamp) + str(block.data) +
                        str(block.previous_hash) + str(block.nonce))
        return hashlib.sha256(block_string.encode()).hexdigest()

    @staticmethod
    def mine_block(block, difficulty):
        """
        Mine a block by finding a hash that meets the difficulty criteria
        """
        while not ProofOfWork.is_valid_hash(ProofOfWork.calculate_hash(block), difficulty):
            block.nonce += 1

    @staticmethod
    def is_valid_hash(hash, difficulty):
        """
        Check if a hash meets the difficulty criteria
        """
        return hash[:difficulty] == '0' * difficulty


# Example usage:
if __name__ == "__main__":
    from src.blockchain.block import Block
    import time

    # Create a block to mine
    block = Block(0, time.time(), "Genesis Block", "0")
    difficulty = 4

    # Mine the block
    ProofOfWork.mine_block(block, difficulty)

    # Print the mined block
    print("Mined Block:")
    print("Index:", block.index)
    print("Timestamp:", block.timestamp)
    print("Data:", block.data)
    print("Previous Hash:", block.previous_hash)
    print("Nonce:", block.nonce)
    print("Hash:", ProofOfWork.calculate_hash(block))

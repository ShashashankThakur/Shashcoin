

class ProofOfWork:

    @staticmethod
    def mine_block(block):
        while block.hash[:block.difficulty] != '0' * block.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()

    @staticmethod
    def is_valid_hash(block):
        """
        Check if a hash meets the difficulty criteria.
        """
        return block.hash[:block.difficulty] == '0' * block.difficulty


# Example usage:
if __name__ == "__main__":
    from src.blockchain.block import Block
    import time

    # Create a block to mine
    block = Block(0, time.time(), "Genesis Block", "0")

    # Print block before mining
    print(block)

    # Mine the block
    ProofOfWork.mine_block(block)

    # Print the mined block
    print(block)

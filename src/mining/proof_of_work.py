

class ProofOfWork:

    @staticmethod
    def mine_block(block, difficulty):
        while block.hash[:difficulty] != '0' * difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()


# Example usage:
if __name__ == "__main__":
    from src.blockchain.block import Block
    import time

    # Create a block to mine
    block = Block(0, time.time(), "Genesis Block", "0")

    # Print block before mining
    print(block)

    difficulty = 4

    # Mine the block
    ProofOfWork.mine_block(block, difficulty)

    # Print the mined block
    print(block)

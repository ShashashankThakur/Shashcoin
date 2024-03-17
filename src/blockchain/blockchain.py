from block import Block
import time


class Blockchain:
    def __init__(self, difficulty):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        """
        Create the genesis block
        """
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        """
        Get the latest block in the blockchain
        """
        return self.chain[-1]

    def add_block(self, new_block):
        """
        Add a new block to the blockchain
        """
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Check if the blockchain is valid by verifying each block's hash and previous hash
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


if __name__ == "__main__":
    blockchain = Blockchain(difficulty=4)

    # Add some blocks to the blockchain
    blockchain.add_block(Block(1, time.time(), "Transaction 1", ""))
    blockchain.add_block(Block(2, time.time(), "Transaction 2", ""))
    blockchain.add_block(Block(3, time.time(), "Transaction 3", ""))

    # Print the blockchain
    for block in blockchain.chain:
        print(block)

    # Check if the blockchain is valid
    print("Is blockchain valid?", blockchain.is_chain_valid())

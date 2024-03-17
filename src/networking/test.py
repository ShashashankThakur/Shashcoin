from node import Node
from src.blockchain.block import Block
from src.blockchain.blockchain import Blockchain
import time
import threading
import pickle


def send_block(node, block):
    node.send_message(pickle.dumps(block))


def receive_block(node):
    data = node.receive_message()
    if data:
        return pickle.loads(data)
    return None


# Start nodes
node1 = Node('localhost', 13000)
node2 = Node('localhost', 13001)
node3 = Node('localhost', 13002)

# Start the nodes in separate threads
node1_thread = threading.Thread(target=node1.start)
node2_thread = threading.Thread(target=node2.start)
node3_thread = threading.Thread(target=node3.start)
node1_thread.start()
node2_thread.start()
node3_thread.start()

# Connect nodes to the network
node1.connect_to_network([('localhost', 13001), ('localhost', 13002)])
node2.connect_to_network([('localhost', 13000), ('localhost', 13002)])
node3.connect_to_network([('localhost', 13000), ('localhost', 13001)])

# Allow some time for connections to be established
time.sleep(1)

# Create and broadcast blocks
blockchain = Blockchain()
block1 = Block(1, time.time(), "Data 1", "0")
print(block1)
block2 = Block(2, time.time(), "Data 2", block1.hash)
print(block2)
block3 = Block(3, time.time(), "Data 3", block2.hash)
print(block3)

threading.Thread(target=send_block, args=(node1, block1)).start()
threading.Thread(target=send_block, args=(node2, block2)).start()
threading.Thread(target=send_block, args=(node3, block3)).start()

# Allow some time for blocks to be received and processed
time.sleep(1)

# Print blockchain for each node
print("Blockchain for Node 1:")
print(block for block in node1.blockchain.chain)
print("Blockchain for Node 2:")
print(block for block in node2.blockchain.chain)
print("Blockchain for Node 3:")
print(block for block in node3.blockchain.chain)

# Close the nodes
node1.close()
node2.close()
node3.close()

# Wait for the threads to finish
node1_thread.join()
node2_thread.join()
node3_thread.join()

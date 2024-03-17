from node import Node
import time
import threading


def send_message(node, message):
    node.send_message(message)


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

# Send messages between nodes
message1 = "Hello from node1"
message2 = "Hello from node2"
message3 = "Hello from node3"

threading.Thread(target=send_message, args=(node1, message1)).start()
threading.Thread(target=send_message, args=(node2, message2)).start()
threading.Thread(target=send_message, args=(node3, message3)).start()

# Allow some time for messages to be received
time.sleep(1)

# Close the nodes
node1.close()
node2.close()
node3.close()

# Wait for the threads to finish
node1_thread.join()
node2_thread.join()
node3_thread.join()

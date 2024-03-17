import socket
import pickle
from datetime import datetime


def time():
    # Return date and time in format
    current_time = datetime.now()
    formatted_time = current_time.strftime("[%Y-%m-%d %H:%M:%S] [SERVER]")
    return formatted_time


def log_print(*args, **kwargs):
    # Print function to include timestamps for logs
    print(f"{time()} ", end='')
    print(*args, **kwargs)


class Node:
    def __init__(self, host, port):
        self.socket = None
        self.host = host
        self.port = port

    def start(self):
        """
        Start the node by creating a socket and listening for connections.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        log_print(f"Node listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.socket.accept()
            log_print(f"Connection established with {addr}")
            data = conn.recv(4096)
            if data:
                message = pickle.loads(data)
                log_print("Received message:", message)
                # Process the received message
                # Example: synchronize blockchain, add new block, etc.
            conn.close()

    def send_message(self, host, port, message):
        """
        Send a message to another node.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(pickle.dumps(message))

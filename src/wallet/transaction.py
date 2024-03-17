import hashlib
import json
import time


class Transaction:
    def __init__(self, sender, recipient, amount, timestamp, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
        self.signature = signature

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

    def sign(self, private_key):
        """
        Sign the transaction using the private key.
        """
        message = json.dumps(self.to_dict(), sort_keys=True)
        self.signature = hashlib.sha256(message.encode()).hexdigest()

    def is_valid(self):
        """
        Verify the signature of the transaction.
        """
        if self.signature is None:
            return False
        message = json.dumps(self.to_dict(), sort_keys=True)
        computed_signature = hashlib.sha256(message.encode()).hexdigest()
        return computed_signature == self.signature


if __name__ == "__main__":

    sender = "sender_public_key"
    recipient = "recipient_public_key"
    amount = 10
    timestamp = time.time()
    private_key = "sender_private_key"

    # Create a transaction
    transaction = Transaction(sender, recipient, amount, timestamp)

    # Sign the transaction
    transaction.sign(private_key)

    # Verify the transaction signature
    print("Is transaction valid?", transaction.is_valid())

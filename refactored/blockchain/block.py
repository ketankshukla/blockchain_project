import hashlib
import json
from typing import List, Union, Dict, Any


class Block:
    """
    Represents a block in the blockchain.
    Each block contains a list of transactions, a reference to the previous block's hash,
    and its own hash calculated based on its contents.
    """
    def __init__(self, index: int, timestamp: float, transactions: Union[str, List[Dict[str, Any]]], 
                previous_hash: str, nonce: int = 0):
        """
        Initialize a new block.
        
        Args:
            index: The position of the block in the chain
            timestamp: Time when the block was created
            transactions: List of transaction records or string (for genesis block)
            previous_hash: Hash of the previous block in the chain
            nonce: Value used in proof-of-work algorithm
        """
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate a SHA-256 hash of the block's contents.
        
        Returns:
            A hexadecimal string representing the hash.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()

    def __str__(self) -> str:
        """String representation of the block."""
        return json.dumps(self.__dict__, indent=4)

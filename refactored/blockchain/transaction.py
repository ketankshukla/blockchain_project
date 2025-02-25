from uuid import uuid4
import time
from typing import Dict, Any, Optional


class Transaction:
    """
    Represents a transaction in the blockchain.
    Each transaction records the transfer of coins from a sender to a receiver.
    """
    def __init__(self, 
                 sender: str, 
                 receiver: str, 
                 amount: float, 
                 timestamp: Optional[float] = None,
                 tx_id: Optional[str] = None,
                 tx_type: Optional[str] = None):
        """
        Initialize a new transaction.
        
        Args:
            sender: Address of the sender
            receiver: Address of the receiver
            amount: Amount of coins transferred
            timestamp: Time when the transaction was created (defaults to current time)
            tx_id: Unique identifier for the transaction (defaults to a new UUID)
            tx_type: Type of transaction (e.g., "sent", "received", "Network Reward")
        """
        self.id = tx_id or str(uuid4())
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.type = tx_type  # Optional field for transaction type
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary for storage.
        
        Returns:
            Dictionary representation of the transaction
        """
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "type": self.type if self.type else None
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """
        Create a Transaction object from a dictionary.
        
        Args:
            data: Dictionary containing transaction data
            
        Returns:
            A new Transaction object
        """
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            amount=data["amount"],
            timestamp=data["timestamp"],
            tx_id=data.get("id"),
            tx_type=data.get("type")
        )
        
    def __str__(self) -> str:
        """String representation of the transaction."""
        return f"Transaction(id={self.id}, sender={self.sender}, receiver={self.receiver}, amount={self.amount})"

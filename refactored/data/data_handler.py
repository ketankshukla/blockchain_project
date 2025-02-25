import json
import os
from typing import Dict, List, Any, Optional


class DataHandler:
    """
    Handles the storage and retrieval of blockchain data, wallets, contacts, and transactions.
    All file operations are centralized in this class to allow for changing storage mechanisms
    in the future (e.g., switching from JSON files to a database).
    """
    def __init__(self, data_dir: str = ""):
        """
        Initialize a data handler with the specified directory for data storage.
        
        Args:
            data_dir: Directory path where data files are stored
        """
        self.data_dir = data_dir
        
        # File paths with directory prefix
        self.wallets_file = os.path.join(data_dir, "wallets.json")
        self.contacts_file = os.path.join(data_dir, "contacts.json")
        self.transactions_dir = os.path.join(data_dir, "transactions")
        self.pending_transactions_file = os.path.join(data_dir, "pending_transactions.json")
        self.completed_transactions_file = os.path.join(data_dir, "completed_transactions.json")
        self.blockchain_file = os.path.join(data_dir, "blockchain.json")
        
        # Ensure transactions directory exists
        os.makedirs(self.transactions_dir, exist_ok=True)
    
    def load_data(self, file_path: str) -> Any:
        """
        Load data from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Loaded data, or empty list if file doesn't exist or is invalid
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_data(self, data: Any, file_path: str) -> None:
        """
        Save data to a JSON file.
        
        Args:
            data: Data to save
            file_path: Path where data will be saved
        """
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_blockchain(self) -> List[Dict[str, Any]]:
        """
        Load blockchain data from storage.
        
        Returns:
            List of dictionaries representing blocks, or empty list if not found
        """
        return self.load_data(self.blockchain_file)
    
    def save_blockchain(self, chain_data: List[Dict[str, Any]]) -> None:
        """
        Save blockchain data to storage.
        
        Args:
            chain_data: List of dictionaries representing blocks
        """
        self.save_data(chain_data, self.blockchain_file)
    
    def load_pending_transactions(self) -> List[Dict[str, Any]]:
        """
        Load pending transactions from storage.
        
        Returns:
            List of pending transactions, or empty list if not found
        """
        return self.load_data(self.pending_transactions_file)
    
    def save_pending_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        """
        Save pending transactions to storage.
        
        Args:
            transactions: List of pending transactions to save
        """
        self.save_data(transactions, self.pending_transactions_file)
    
    def load_completed_transactions(self) -> List[Dict[str, Any]]:
        """
        Load completed transactions from storage.
        
        Returns:
            List of completed transactions, or empty list if not found
        """
        return self.load_data(self.completed_transactions_file)
    
    def save_completed_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        """
        Save completed transactions to storage.
        
        Args:
            transactions: List of completed transactions to save
        """
        self.save_data(transactions, self.completed_transactions_file)
    
    def load_wallets(self) -> List[Dict[str, Any]]:
        """
        Load wallet data from storage.
        
        Returns:
            List of wallets, or empty list if not found
        """
        return self.load_data(self.wallets_file)
    
    def save_wallets(self, wallets: List[Dict[str, Any]]) -> None:
        """
        Save wallet data to storage.
        
        Args:
            wallets: List of wallets to save
        """
        self.save_data(wallets, self.wallets_file)
    
    def load_contacts(self) -> List[Dict[str, Any]]:
        """
        Load contact data from storage.
        
        Returns:
            List of contacts, or empty list if not found
        """
        return self.load_data(self.contacts_file)
    
    def save_contacts(self, contacts: List[Dict[str, Any]]) -> None:
        """
        Save contact data to storage.
        
        Args:
            contacts: List of contacts to save
        """
        self.save_data(contacts, self.contacts_file)
    
    def get_transaction_file(self, wallet_address: str) -> str:
        """
        Get the path to a wallet's transaction history file.
        
        Args:
            wallet_address: Address of the wallet
            
        Returns:
            Path to the wallet's transaction file
        """
        return os.path.join(self.transactions_dir, f"transactions_{wallet_address}.json")
    
    def record_transaction(self, transaction: Dict[str, Any], wallet_address: str, tx_type: str = "transaction") -> None:
        """
        Record a transaction in a wallet's transaction history.
        
        Args:
            transaction: Transaction data to record
            wallet_address: Address of the wallet
            tx_type: Type of transaction ("sent", "received", or "Network Reward")
        """
        tx_file = self.get_transaction_file(wallet_address)
        transactions = self.load_data(tx_file)
        
        # Add type and block time if not present
        tx_copy = transaction.copy()
        if "type" not in tx_copy:
            if tx_type == "Network Reward":
                tx_copy["type"] = "reward"
            elif wallet_address == tx_copy["sender"]:
                tx_copy["type"] = "sent"
            else:
                tx_copy["type"] = "received"
        
        if "block_time" not in tx_copy:
            tx_copy["block_time"] = transaction.get("timestamp")
            
        transactions.append(tx_copy)
        self.save_data(transactions, tx_file)
    
    def update_wallet_balance(self, address: str, amount_change: float) -> None:
        """
        Update a wallet's balance.
        
        Args:
            address: Address of the wallet
            amount_change: Amount to change (positive for receiving, negative for sending)
        """
        wallets = self.load_wallets()
        for wallet in wallets:
            if wallet["address"] == address:
                wallet["balance"] = wallet.get("balance", 0) + amount_change
                self.save_wallets(wallets)
                return
        
        # If wallet not found, print error
        print(f"Error: Wallet with address {address} not found")
    
    def name_exists_in_contacts(self, first_name: str, last_name: str) -> bool:
        """
        Check if a contact with the given name already exists.
        
        Args:
            first_name: First name to check
            last_name: Last name to check
            
        Returns:
            True if a contact with the name exists, False otherwise
        """
        contacts = self.load_contacts()
        for contact in contacts:
            if (contact["first_name"].lower() == first_name.lower() and 
                contact["last_name"].lower() == last_name.lower()):
                return True
        return False

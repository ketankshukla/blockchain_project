from typing import Dict, Any
from uuid import uuid4
from tabulate import tabulate
from utils.formatting import (
    format_address_with_name, format_amount, format_timestamp, format_hash
)


class BlockchainUI:
    """
    User interface for blockchain-related operations like mining blocks and viewing blockchain data.
    """
    def __init__(self, data_handler, blockchain):
        """
        Initialize the blockchain UI with data handler and blockchain.
        
        Args:
            data_handler: Handler for storing and retrieving blockchain data
            blockchain: The blockchain instance to interact with
        """
        self.data_handler = data_handler
        self.blockchain = blockchain
    
    def mine_transactions(self, current_wallet: Dict[str, Any]) -> bool:
        """
        Display UI for mining pending transactions.
        
        Args:
            current_wallet: Wallet that will receive the mining reward
            
        Returns:
            True if mining was successful, False otherwise
        """
        print("\nMining pending transactions...")
        pending_count = len(self.blockchain.pending_transactions)
        
        if pending_count == 0:
            print("No transactions available for mining.")
            return False
            
        print(f"Pending transactions: {pending_count}")
        confirm = input("\nStart mining? (press Enter to cancel): ").strip()
        if not confirm:
            print("Mining cancelled - Returning to main menu")
            return False
        
        try:
            processed_count = self.blockchain.mine_pending_transactions(current_wallet['address'])
            print(f"\nBlock mined successfully! {processed_count} transactions processed.")
            print(f"Mining reward: {self.blockchain.mining_reward} coins added to your wallet")
            
            # Record reward transaction separately since it's handled in blockchain.mine_pending_transactions
            return True
        except ValueError as e:
            print(f"\nMining failed: {str(e)}")
            return False
        except Exception as e:
            print(f"\nMining failed: {str(e)}")
            return False
    
    def view_blockchain(self) -> None:
        """
        Display UI for viewing blockchain information and blocks.
        """
        print("\n=== Blockchain Info ===")
        print(f" Chain length: {len(self.blockchain.chain)} blocks")
        print(f" Pending transactions: {len(self.blockchain.pending_transactions)}")
        print(f" Chain validity: {'Valid' if self.blockchain.validate_chain() else 'Invalid'}")
        
        view_details = input("\nView block details? (press Enter to skip): ").strip()
        if not view_details:
            return
            
        # Load contacts and wallets for address display
        contacts = self.data_handler.load_contacts()
        wallets = self.data_handler.load_wallets()
        
        for i, block in enumerate(self.blockchain.chain):
            print(f"\n Block #{i}")
            print("=" * 50)
            
            # Basic block info
            block_info = [
                ["Index", str(block.index).center(10)],
                ["Timestamp", format_timestamp(block.timestamp)],
                ["Previous Hash", format_hash(block.previous_hash)],
                ["Hash", format_hash(block.hash)],
                ["Nonce", str(block.nonce).center(10)]
            ]
            print(tabulate(block_info, tablefmt="simple_grid"))
            
            # If it's not the genesis block, show transactions
            if isinstance(block.transactions, list):
                if block.transactions:
                    print("\nTransactions:")
                    tx_data = []
                    
                    for tx in block.transactions:
                        # For reward transactions, use "Network Reward" as sender
                        if isinstance(tx, dict) and tx.get('type') == 'REWARD':
                            sender = "Network Reward"
                        else:
                            sender = format_address_with_name(
                                tx['sender'] if isinstance(tx, dict) else tx.sender,
                                contacts,
                                wallets,
                                is_sender=True
                            )
                        
                        # Get receiver with name
                        receiver = format_address_with_name(
                            tx['receiver'] if isinstance(tx, dict) else tx.receiver,
                            contacts,
                            wallets
                        )
                        
                        # Get amount and time
                        amount = tx['amount'] if isinstance(tx, dict) else tx.amount
                        timestamp = tx['timestamp'] if isinstance(tx, dict) else tx.timestamp
                        
                        tx_data.append([
                            sender,
                            receiver,
                            format_amount(amount),
                            format_timestamp(timestamp)
                        ])
                    
                    print(tabulate(tx_data, 
                                headers=['From'.center(36), 'To'.center(36), 
                                        'Amount'.center(14), 'Time'.center(21)],
                                tablefmt="simple_grid"))
                else:
                    print("No transactions in this block")
            print("\n")

from typing import Dict, List, Any, Optional
from tabulate import tabulate
from utils.validation import get_valid_input, validate_positive_number
from utils.formatting import (
    format_address_with_name, format_amount, format_timestamp, 
    format_type, pad_to_width
)


class TransactionUI:
    """
    User interface for transaction-related operations like sending transactions and
    viewing transaction history.
    """
    def __init__(self, data_handler, blockchain):
        """
        Initialize the transaction UI with data handler and blockchain.
        
        Args:
            data_handler: Handler for storing and retrieving transaction data
            blockchain: The blockchain instance to interact with
        """
        self.data_handler = data_handler
        self.blockchain = blockchain
    
    def send_transaction(self, current_wallet: Dict[str, Any]) -> bool:
        """
        Display UI for sending a transaction from the current wallet to another wallet.
        
        Args:
            current_wallet: The sender's wallet
            
        Returns:
            True if transaction was successful, False otherwise
        """
        sender_address = current_wallet['address']
        sender_balance = current_wallet['balance']
        
        print("\n=== Send Transaction ===")
        print(f"Your balance: {sender_balance}")
        
        if sender_balance <= 0:
            print("Insufficient balance to send a transaction.")
            return False
        
        # Load contacts to display as recipients
        contacts = self.data_handler.load_contacts()
        if not contacts:
            print("No contacts available. Please add contacts first.")
            return False
        
        # Filter out the current wallet from the contacts list
        filtered_contacts = [c for c in contacts if c["address"] != sender_address]
        if not filtered_contacts:
            print("No contacts available to send to. Please add contacts first.")
            return False
        
        print("\nSelect Recipient:")
        for i, contact in enumerate(filtered_contacts, 1):
            print(f"{i}. {contact['first_name']} {contact['last_name']}")
        
        print("X - Cancel")
        
        choice = input("\nEnter recipient number or X to cancel: ").strip().upper()
        if choice == 'X':
            print("Transaction cancelled.")
            return False
        
        try:
            recipient_index = int(choice) - 1
            if 0 <= recipient_index < len(filtered_contacts):
                recipient = filtered_contacts[recipient_index]
                recipient_address = recipient["address"]
                
                # Ask for amount
                amount_str = get_valid_input(
                    f"Enter amount to send to {recipient['first_name']} (max {sender_balance}): ",
                    lambda x: validate_positive_number(x) and float(x) <= sender_balance,
                    f"Invalid amount. Please enter a positive number not exceeding {sender_balance}."
                )
                amount = float(amount_str)
                
                # Confirm transaction
                print("\nTransaction Details:")
                print(f"From: {current_wallet.get('nickname', 'Your Wallet')}")
                print(f"To: {recipient['first_name']} {recipient['last_name']}")
                print(f"Amount: {amount}")
                
                confirm = input("\nConfirm transaction? (y/n): ").strip().lower()
                if confirm != 'y':
                    print("Transaction cancelled.")
                    return False
                
                # Create the transaction
                transaction = self.blockchain.create_transaction(sender_address, recipient_address, amount)
                
                # Update wallet balances
                self.data_handler.update_wallet_balance(sender_address, -amount)
                self.data_handler.update_wallet_balance(recipient_address, amount)
                
                # Record transaction for sender and recipient
                self.data_handler.record_transaction(transaction, sender_address, "sent")
                self.data_handler.record_transaction(transaction, recipient_address, "received")
                
                print("\nTransaction completed successfully!")
                return True
            else:
                print("Invalid recipient selection.")
                return False
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return False
    
    def view_transaction_history(self, wallet_address: Optional[str] = None) -> None:
        """
        Display UI for viewing transaction history for a wallet.
        
        Args:
            wallet_address: Address of the wallet to view history for.
                            If None, user will be prompted to select a wallet.
        """
        if not wallet_address:
            wallets = self.data_handler.load_wallets()
            
            print("\n=== View Transaction History ===")
            print("Select Wallet:")
            
            for i, wallet in enumerate(wallets, 1):
                print(f"{i}. {wallet.get('nickname', 'Wallet')} - Balance: {wallet['balance']}")
            
            try:
                wallet_index = int(input("\nEnter wallet number: ")) - 1
                if 0 <= wallet_index < len(wallets):
                    wallet_address = wallets[wallet_index]["address"]
                else:
                    print("Invalid wallet selection.")
                    return
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                return
        
        # Load wallet's transactions
        tx_file = self.data_handler.get_transaction_file(wallet_address)
        transactions = self.data_handler.load_data(tx_file)
        
        # Find wallet nickname
        wallets = self.data_handler.load_wallets()
        wallet_nickname = None
        for wallet in wallets:
            if wallet["address"] == wallet_address:
                wallet_nickname = wallet.get("nickname", "Selected Wallet")
                break
        
        print(f"\n Transaction History for {wallet_nickname}")
        print("=" * 50)
        
        if not transactions:
            print("\n No transactions found")
            return
        
        # Load contacts and wallets for display
        contacts = self.data_handler.load_contacts()
        
        # Prepare headers with exact widths
        headers = [
            pad_to_width('Type', 14),
            pad_to_width('Amount', 14),
            pad_to_width('From', 50),
            pad_to_width('To', 50),
            pad_to_width('Time', 21)
        ]
        
        # Ensure all data rows have exact widths
        tx_data = []
        for tx in transactions:
            tx_type = tx.get('type', 'UNKNOWN')
            tx_type = tx_type.upper() if tx_type else 'UNKNOWN'
            tx_data.append([
                format_type(tx_type),
                format_amount(tx['amount']),
                format_address_with_name(tx['sender'], contacts, wallets, is_sender=True),
                format_address_with_name(tx['receiver'], contacts, wallets, is_sender=False),
                format_timestamp(tx['timestamp'])
            ])
        
        print("\n" + tabulate(tx_data,
                       headers=headers,
                       tablefmt="simple_grid",
                       colalign=("center", "center", "center", "center", "center"),
                       disable_numparse=True) + "\n")
    
    def view_contact_transactions(self) -> None:
        """
        Display UI for viewing a specific contact's transaction history.
        """
        contacts = self.data_handler.load_contacts()
        if not contacts:
            print("\nNo contacts available!")
            return
        
        print("\nSelect Contact:")
        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact['first_name']} {contact['last_name']}")
        
        try:
            contact_index = int(input("\nEnter contact number: ")) - 1
            if 0 <= contact_index < len(contacts):
                contact = contacts[contact_index]
                tx_file = self.data_handler.get_transaction_file(contact['address'])
                transactions = self.data_handler.load_data(tx_file)
                
                print(f"\nTransactions for {contact['first_name']} {contact['last_name']}:")
                if not transactions:
                    print(" No transactions found")
                else:
                    for tx in transactions:
                        tx_type = tx.get('type', 'UNKNOWN')
                        tx_type = tx_type.upper() if tx_type else 'UNKNOWN'
                        print(f"\n{format_timestamp(tx['timestamp'])} - {tx_type}: {tx['amount']} coins")
                        print(f" From: {tx['sender']}")
                        print(f" To: {tx['receiver']}")
            else:
                print(" Invalid contact selection")
        except ValueError:
            print(" Please enter a valid number")

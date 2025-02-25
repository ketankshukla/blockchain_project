#!/usr/bin/env python
"""
Simple Blockchain Application
----------------------------
This application provides a command-line interface for interacting with
a simple blockchain implementation, allowing for wallet management,
transaction sending, block mining, and more.
"""

import os
import sys
import traceback

with open('app_log.txt', 'w') as f:
    f.write("Starting blockchain application log...\n")

try:
    # Add the current directory to the Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from blockchain.blockchain import Blockchain
    from data.data_handler import DataHandler
    from ui.wallet_ui import WalletUI
    from ui.transaction_ui import TransactionUI
    from ui.blockchain_ui import BlockchainUI
    from ui.contacts_ui import ContactsUI
    
    with open('app_log.txt', 'a') as f:
        f.write("Successfully imported all modules\n")
except Exception as e:
    with open('app_log.txt', 'a') as f:
        f.write(f"Error during import: {str(e)}\n")
        f.write(traceback.format_exc())
    raise

print("Starting blockchain application...")

class BlockchainApp:
    """
    Main application class that ties together all components.
    """
    def __init__(self):
        """Initialize the application with all required components."""
        # Set up data directory - using parent directory for compatibility with original data
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(self.base_dir)
        
        # Create data handler pointing to parent directory for data
        self.data_handler = DataHandler(self.parent_dir)
        
        # Initialize blockchain
        self.blockchain = Blockchain(self.data_handler)
        
        # Initialize UI components
        self.wallet_ui = WalletUI(self.data_handler)
        self.transaction_ui = TransactionUI(self.data_handler, self.blockchain)
        self.blockchain_ui = BlockchainUI(self.data_handler, self.blockchain)
        self.contacts_ui = ContactsUI(self.data_handler)
        
        # Initialize current wallet
        self.current_wallet = None

    def run(self):
        """
        Run the main application loop, displaying the menu and processing user input.
        """
        while True:
            # Wallet selection/creation
            if not self.current_wallet:
                wallet = self.wallet_ui.select_wallet()
                if not wallet:
                    print("\nPlease select or create a wallet to continue")
                    continue
                self.current_wallet = wallet

            # Display current user info
            print("\n" + "="*50)
            # Handle both old and new wallet formats
            if 'first_name' in self.current_wallet and 'last_name' in self.current_wallet:
                user_name = f"{self.current_wallet['first_name']} {self.current_wallet['last_name']}"
            else:
                user_name = self.current_wallet['nickname']
            print(f"Current User: {user_name}")
            print(f"Balance: {self.current_wallet['balance']}")
            print("="*50)

            print("\n=== Blockchain Main Menu ===")
            print("1. Send Transaction")
            print("2. Mine Transactions")
            print("3. View Blockchain")
            print("4. View My Transactions")
            print("5. View Contact Transactions")
            print("6. Manage Contacts")
            print("7. Switch Wallet")
            print("8. Exit")

            choice = input("\nEnter choice (1-8): ").strip()
            if not choice:
                continue  # In main menu, Enter just refreshes the menu

            try:
                if choice == '1':
                    # Validate wallet and contacts
                    if not self.current_wallet:
                        print("\n Please select or create a wallet first!")
                        continue

                    contacts = self.data_handler.load_contacts()
                    if not contacts:
                        print("\n No contacts available! Please add contacts first.")
                        continue

                    self.transaction_ui.send_transaction(self.current_wallet)

                elif choice == '2':
                    if not self.current_wallet:
                        print("\n Please select or create a wallet first!")
                        continue

                    self.blockchain_ui.mine_transactions(self.current_wallet)
                    # Reload wallet to get updated balance
                    wallets = self.data_handler.load_wallets()
                    for wallet in wallets:
                        if wallet["address"] == self.current_wallet["address"]:
                            self.current_wallet = wallet
                            break

                elif choice == '3':
                    self.blockchain_ui.view_blockchain()

                elif choice == '4':
                    if not self.current_wallet:
                        print("\n No wallet selected!")
                        continue
                        
                    self.transaction_ui.view_transaction_history(self.current_wallet['address'])

                elif choice == '5':
                    self.transaction_ui.view_contact_transactions()

                elif choice == '6':
                    self.contacts_ui.manage_contacts()

                elif choice == '7':
                    self.current_wallet = self.wallet_ui.select_wallet()

                elif choice == '8':
                    print("\n Exiting...")
                    sys.exit(0)

                else:
                    print("\n Invalid choice")

            except Exception as e:
                with open('app_log.txt', 'a') as f:
                    f.write(f"Error during execution: {str(e)}\n")
                    f.write(traceback.format_exc())
                print(f"\n Error: {str(e)}")
                
            # Wait for user to press Enter before continuing
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        with open('app_log.txt', 'a') as f:
            f.write("Creating and running BlockchainApp\n")
        app = BlockchainApp()
        app.run()
    except Exception as e:
        with open('app_log.txt', 'a') as f:
            f.write(f"Fatal error: {str(e)}\n")
            f.write(traceback.format_exc())
        print(f"Fatal error: {str(e)}")

from uuid import uuid4
from typing import Dict, List, Any, Optional, Tuple
from utils.validation import get_valid_input, validate_name, validate_non_empty


class WalletUI:
    """
    User interface for wallet-related operations like creating wallets and selecting wallets.
    """
    def __init__(self, data_handler):
        """
        Initialize the wallet UI with a data handler.
        
        Args:
            data_handler: Handler for storing and retrieving wallet data
        """
        self.data_handler = data_handler
    
    def select_wallet(self) -> Optional[Dict[str, Any]]:
        """
        Display UI for selecting an existing wallet or creating a new one.
        
        Returns:
            Selected wallet or None if operation was cancelled
        """
        wallets = self.data_handler.load_wallets()
        
        print("\n=== Select Wallet ===")
        print(f"Found {len(wallets)} wallet(s)")
        
        if wallets:
            print("\nExisting Wallets:")
            for i, wallet in enumerate(wallets, 1):
                if 'nickname' in wallet:
                    print(f"{i}. {wallet['nickname']} - Balance: {wallet['balance']}")
                else:
                    # Handle older wallet format
                    name = f"{wallet.get('first_name', '')} {wallet.get('last_name', '')}".strip()
                    print(f"{i}. {name} - Balance: {wallet['balance']}")
            
            print("\nOptions:")
            print("Enter wallet number to select")
            print("N - Create New Wallet")
            print("X - Cancel")
            
            choice = input("\nEnter choice: ").strip().upper()
            
            if choice == 'N':
                return self.create_wallet()
            elif choice == 'X':
                return None
            else:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(wallets):
                        return wallets[index]
                    else:
                        print("Invalid wallet number")
                        return self.select_wallet()  # Recursive call for retry
                except ValueError:
                    print("Invalid input")
                    return self.select_wallet()  # Recursive call for retry
        else:
            print("\nNo wallets found.")
            create_new = input("Create a new wallet? (y/n): ").strip().lower()
            if create_new == 'y':
                return self.create_wallet()
            else:
                return None
    
    def create_wallet(self) -> Optional[Dict[str, Any]]:
        """
        Display UI for creating a new wallet and corresponding contact.
        
        Returns:
            Newly created wallet or None if operation was cancelled
        """
        print("\n=== Create New Wallet ===")
        
        # Ask for first and last name
        first_name = get_valid_input(
            "Enter First Name: ",
            validate_name,
            "Invalid first name. Must contain only letters and be at least 2 characters."
        )
        
        last_name = get_valid_input(
            "Enter Last Name: ",
            validate_name,
            "Invalid last name. Must contain only letters and be at least 2 characters."
        )
        
        # Check if contact with this name already exists
        if self.data_handler.name_exists_in_contacts(first_name, last_name):
            print(f"\nA contact with the name {first_name} {last_name} already exists.")
            print("Please use a different name for your wallet.")
            return self.create_wallet()  # Recursive call for retry
        
        # Generate a new wallet address
        address = str(uuid4().hex)
        
        # Create nickname (combination of first and last name)
        nickname = f"{first_name} {last_name}"
        
        # Create and save the new wallet
        new_wallet = {
            "address": address,
            "nickname": nickname,
            "balance": 100  # Starting balance for new wallets
        }
        
        # Save wallet
        wallets = self.data_handler.load_wallets()
        wallets.append(new_wallet)
        self.data_handler.save_wallets(wallets)
        
        # Add as a contact
        new_contact = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address
        }
        
        contacts = self.data_handler.load_contacts()
        contacts.append(new_contact)
        self.data_handler.save_contacts(contacts)
        
        print(f"\nWallet created successfully for {first_name} {last_name}")
        print(f"Address: {address}")
        print(f"Starting Balance: {new_wallet['balance']}")
        
        return new_wallet

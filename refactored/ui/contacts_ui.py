from uuid import uuid4
from typing import Dict, List, Any, Optional
from utils.validation import get_valid_input, validate_name


class ContactsUI:
    """
    User interface for managing contacts like adding, editing, and deleting contacts.
    """
    def __init__(self, data_handler):
        """
        Initialize the contacts UI with a data handler.
        
        Args:
            data_handler: Handler for storing and retrieving contact data
        """
        self.data_handler = data_handler
    
    def manage_contacts(self) -> None:
        """
        Display UI for managing contacts (add, delete, edit).
        """
        while True:
            print("\n=== Manage Contacts ===")
            
            contacts = self.data_handler.load_contacts()
            print(f"Found {len(contacts)} contact(s)")
            
            if contacts:
                print("\nExisting Contacts:")
                for i, contact in enumerate(contacts, 1):
                    print(f"{i}. {contact['first_name']} {contact['last_name']}")
            
            print("\nOptions:")
            print("1. Add New Contact")
            print("2. Delete Contact")
            print("3. Edit Contact")
            print("4. Return to Main Menu")
            
            choice = input("\nEnter option (1-4): ").strip()
            
            if choice == '1':
                self._add_contact()
            elif choice == '2':
                self._delete_contact(contacts)
            elif choice == '3':
                self._edit_contact(contacts)
            elif choice == '4':
                break
            else:
                print("Invalid option. Please try again.")
    
    def _add_contact(self) -> None:
        """
        Display UI for adding a new contact.
        """
        print("\n=== Add New Contact ===")
        
        # Get first and last name
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
        
        # Check if name already exists
        if self.data_handler.name_exists_in_contacts(first_name, last_name):
            print(f"\nA contact with the name {first_name} {last_name} already exists.")
            return
        
        # Generate a unique address for the contact
        address = str(uuid4().hex)
        
        # Create the new contact
        new_contact = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address
        }
        
        # Save the new contact
        contacts = self.data_handler.load_contacts()
        contacts.append(new_contact)
        self.data_handler.save_contacts(contacts)
        
        print(f"\nContact added: {first_name} {last_name}")
        print(f"Address: {address}")
    
    def _delete_contact(self, contacts: List[Dict[str, Any]]) -> None:
        """
        Display UI for deleting an existing contact.
        
        Args:
            contacts: List of existing contacts
        """
        if not contacts:
            print("\nNo contacts to delete.")
            return
        
        print("\n=== Delete Contact ===")
        print("Select contact to delete:")
        
        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact['first_name']} {contact['last_name']}")
        
        print("X - Cancel")
        
        choice = input("\nEnter contact number or X to cancel: ").strip().upper()
        if choice == 'X':
            return
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(contacts):
                contact = contacts[index]
                
                # Confirm deletion
                confirm = input(f"Are you sure you want to delete {contact['first_name']} {contact['last_name']}? (y/n): ").strip().lower()
                if confirm == 'y':
                    # Check if the contact is also a wallet
                    wallets = self.data_handler.load_wallets()
                    is_wallet = False
                    
                    for wallet in wallets:
                        if wallet.get("address") == contact["address"]:
                            is_wallet = True
                            break
                    
                    if is_wallet:
                        print("\nThis contact is associated with a wallet and cannot be deleted.")
                        print("You can delete the wallet instead, which will also remove the contact.")
                        return
                    
                    # Delete the contact
                    contacts.pop(index)
                    self.data_handler.save_contacts(contacts)
                    print(f"\nContact {contact['first_name']} {contact['last_name']} deleted.")
                else:
                    print("\nDeletion cancelled.")
            else:
                print("\nInvalid contact number.")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
    
    def _edit_contact(self, contacts: List[Dict[str, Any]]) -> None:
        """
        Display UI for editing an existing contact.
        
        Args:
            contacts: List of existing contacts
        """
        if not contacts:
            print("\nNo contacts to edit.")
            return
        
        print("\n=== Edit Contact ===")
        print("Select contact to edit:")
        
        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact['first_name']} {contact['last_name']}")
        
        print("X - Cancel")
        
        choice = input("\nEnter contact number or X to cancel: ").strip().upper()
        if choice == 'X':
            return
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(contacts):
                contact = contacts[index]
                
                print(f"\nEditing contact: {contact['first_name']} {contact['last_name']}")
                print("Enter new information (leave blank to keep current value)")
                
                # Get new first name
                new_first_name = input(f"First Name [{contact['first_name']}]: ").strip()
                if new_first_name and not validate_name(new_first_name):
                    print("Invalid first name. Must contain only letters and be at least 2 characters.")
                    return
                
                # Get new last name
                new_last_name = input(f"Last Name [{contact['last_name']}]: ").strip()
                if new_last_name and not validate_name(new_last_name):
                    print("Invalid last name. Must contain only letters and be at least 2 characters.")
                    return
                
                # Use current values if new ones not provided
                first_name = new_first_name if new_first_name else contact['first_name']
                last_name = new_last_name if new_last_name else contact['last_name']
                
                # Check if the new name combination already exists
                if (first_name != contact['first_name'] or last_name != contact['last_name']) and \
                   self.data_handler.name_exists_in_contacts(first_name, last_name):
                    print(f"\nA contact with the name {first_name} {last_name} already exists.")
                    return
                
                # Update the contact
                contact['first_name'] = first_name
                contact['last_name'] = last_name
                self.data_handler.save_contacts(contacts)
                
                # If this contact is also a wallet, update the wallet nickname
                wallets = self.data_handler.load_wallets()
                for wallet in wallets:
                    if wallet.get("address") == contact["address"]:
                        wallet["nickname"] = f"{first_name} {last_name}"
                        self.data_handler.save_wallets(wallets)
                        break
                
                print(f"\nContact updated: {first_name} {last_name}")
            else:
                print("\nInvalid contact number.")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

import hashlib
import json
import os
import time
from uuid import uuid4
from tabulate import tabulate
from datetime import datetime
import unicodedata

# File paths
WALLETS_FILE = "wallets.json"
CONTACTS_FILE = "contacts.json"
TRANSACTIONS_DIR = "transactions"
PENDING_TRANSACTIONS_FILE = "pending_transactions.json"
COMPLETED_TRANSACTIONS_FILE = "completed_transactions.json"
BLOCKCHAIN_FILE = "blockchain.json"

os.makedirs(TRANSACTIONS_DIR, exist_ok=True)

def get_valid_input(prompt, validation_func, error_message):
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        print(error_message)

def get_string_width(s):
    """Get the display width of a string, counting emoji as 2 characters"""
    width = 0
    for c in s:
        # East Asian Width property
        if unicodedata.east_asian_width(c) in ('F', 'W'):
            width += 2
        else:
            width += 1
    return width

def pad_to_width(s, width):
    """Pad a string to exact width, considering emoji width"""
    current_width = get_string_width(s)
    if current_width < width:
        padding = width - current_width
        left_pad = padding // 2
        right_pad = padding - left_pad
        return ' ' * left_pad + s + ' ' * right_pad
    return s

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)

class Blockchain:
    def __init__(self):
        self.difficulty = 4
        self.mining_reward = 10
        self.chain = self.load_blockchain()
        if not self.chain:
            self.chain = [self.create_genesis_block()]
            self.save_blockchain()
        self.load_pending_transactions()

    def load_blockchain(self):
        try:
            # First try to load existing blockchain
            chain_data = load_data(BLOCKCHAIN_FILE)
            if chain_data:
                print("Loading existing blockchain...")
                # Convert dictionary objects back to Block objects
                chain = [Block(
                    block['index'],
                    block['timestamp'],
                    block['transactions'],
                    block['previous_hash'],
                    block['nonce']
                ) for block in chain_data]
                
                # Recalculate all block hashes to ensure chain integrity
                for i in range(len(chain)):
                    if i == 0:  # Genesis block
                        chain[i].hash = chain[i].calculate_hash()
                    else:
                        # Ensure previous_hash is correct
                        chain[i].previous_hash = chain[i-1].hash
                        # Recalculate current block's hash
                        chain[i].hash = chain[i].calculate_hash()
                
                # Save the chain with updated hashes
                self.chain = chain
                self.save_blockchain()
                return chain
            
            print("No blockchain file found, reconstructing from completed transactions...")
            # If no blockchain file exists, reconstruct from completed transactions
            completed_transactions = load_data(COMPLETED_TRANSACTIONS_FILE)
            if not completed_transactions:
                print("No completed transactions found.")
                return []
                
            print(f"Found {len(completed_transactions)} completed transactions")
            
            # Group transactions by mining rewards
            chain = [self.create_genesis_block()]
            current_block_txs = []
            
            for tx in completed_transactions:
                current_block_txs.append(tx)
                # When we find a reward transaction, that marks the end of a block
                if tx.get('type') == 'REWARD':
                    # Create a new block with these transactions
                    new_block = Block(
                        len(chain),
                        tx['timestamp'],  # Use reward transaction timestamp
                        current_block_txs,
                        chain[-1].hash
                    )
                    new_block.hash = new_block.calculate_hash()
                    chain.append(new_block)
                    current_block_txs = []  # Start a new block
            
            # If any transactions left without a reward, add them as a final block
            if current_block_txs:
                new_block = Block(
                    len(chain),
                    current_block_txs[-1]['timestamp'],
                    current_block_txs,
                    chain[-1].hash
                )
                new_block.hash = new_block.calculate_hash()
                chain.append(new_block)
            
            print(f"Created blockchain with {len(chain)} blocks")
            
            # Save the reconstructed chain
            self.chain = chain
            self.save_blockchain()
            return chain
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading blockchain: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return []

    def save_blockchain(self):
        try:
            # Convert Block objects to dictionaries for JSON serialization
            chain_data = [{
                'index': block.index,
                'timestamp': block.timestamp,
                'transactions': block.transactions,
                'previous_hash': block.previous_hash,
                'nonce': block.nonce,
                'hash': block.hash
            } for block in self.chain]
            save_data(chain_data, BLOCKCHAIN_FILE)
            print(f"Saved blockchain with {len(chain_data)} blocks")
        except Exception as e:
            print(f"Error saving blockchain: {str(e)}")

    def load_pending_transactions(self):
        try:
            with open(PENDING_TRANSACTIONS_FILE, 'r') as f:
                self.pending_transactions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.pending_transactions = []
            self.save_pending_transactions()

    def save_pending_transactions(self):
        with open(PENDING_TRANSACTIONS_FILE, 'w') as f:
            json.dump(self.pending_transactions, f, indent=2)

    def load_completed_transactions(self):
        try:
            with open(COMPLETED_TRANSACTIONS_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_completed_transactions(self, transactions):
        completed = self.load_completed_transactions()
        completed.extend(transactions)
        with open(COMPLETED_TRANSACTIONS_FILE, 'w') as f:
            json.dump(completed, f, indent=2)

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def create_transaction(self, sender, receiver, amount):
        transaction = {
            "id": str(uuid4()),
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": time.time()
        }
        self.pending_transactions.append(transaction)
        self.save_pending_transactions()
        return transaction

    def mine_pending_transactions(self, miner_address):
        """Mine pending transactions and create a new block"""
        # Load pending transactions
        pending_transactions = load_data(PENDING_TRANSACTIONS_FILE)
        if not pending_transactions:
            return 0  # Return number of transactions processed instead of False

        # Create mining reward transaction
        reward_transaction = {
            'sender': "Network Reward",
            'receiver': miner_address,
            'amount': self.mining_reward,
            'timestamp': time.time(),
            'type': 'REWARD'
        }

        # Create new block with pending transactions and reward
        new_block = Block(
            len(self.chain),
            time.time(),
            pending_transactions + [reward_transaction],
            self.chain[-1].hash if self.chain else "0"
        )

        # Mine the block
        new_block.nonce = self.proof_of_work(new_block)
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        self.save_blockchain()  # Save the updated chain

        # Update completed transactions
        completed_transactions = load_data(COMPLETED_TRANSACTIONS_FILE)
        completed_transactions.extend(pending_transactions + [reward_transaction])
        save_data(completed_transactions, COMPLETED_TRANSACTIONS_FILE)

        # Clear pending transactions
        save_data([], PENDING_TRANSACTIONS_FILE)
        self.pending_transactions = []

        # Update miner's wallet with reward
        update_wallet_balance(miner_address, self.mining_reward)

        return len(pending_transactions)  # Return number of transactions processed

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.calculate_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.calculate_hash()
        return block.nonce

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_transaction_file(wallet_address):
    return os.path.join(TRANSACTIONS_DIR, f"transactions_{wallet_address}.json")

def record_transaction(transaction, wallet_address, tx_type="transaction"):
    """Record a transaction in the wallet's transaction history"""
    tx_file = get_transaction_file(wallet_address)
    transactions = load_data(tx_file)
    transactions.append({
        **transaction,
        "type": "Network Reward" if tx_type == "Network Reward" else "Transaction",
        "block_time": time.time()
    })
    save_data(transactions, tx_file)

def update_wallet_balance(address, amount_change):
    """Update a wallet's balance. Positive amount_change for receiving, negative for sending."""
    wallets = load_data(WALLETS_FILE)
    for wallet in wallets:
        if wallet['address'] == address:
            wallet['balance'] += amount_change
            save_data(wallets, WALLETS_FILE)
            return True
    return False

def name_exists_in_contacts(first_name, last_name):
    """Check if a contact with the given name already exists"""
    contacts = load_data(CONTACTS_FILE)
    return any(
        contact['first_name'].lower() == first_name.lower() and 
        contact['last_name'].lower() == last_name.lower() 
        for contact in contacts
    )

def select_wallet():
    """Select an existing wallet or create a new one"""
    while True:
        wallets = load_data(WALLETS_FILE)
        if not wallets:
            print("\nNo wallets found. Creating new wallet...")
            return create_wallet()

        print("\n=== Select Wallet ===")
        for i, wallet in enumerate(wallets, 1):
            print(f"{i}. {wallet['nickname']}")
        print("3. Create New Wallet")
        print("\nPress Enter to return to main menu")

        choice = input("\nEnter choice (1-3): ").strip()
        if not choice:
            return None

        try:
            choice_num = int(choice)
            if choice_num == 3:
                return create_wallet()
            
            wallet_index = choice_num - 1
            if 0 <= wallet_index < len(wallets):
                return wallets[wallet_index]
            
            print("Invalid choice")
        except ValueError:
            print("Invalid input")

def create_wallet():
    """Create a new wallet and corresponding contact"""
    print("\n=== Create New Wallet ===")
    print("Enter wallet details (press Enter to return):")
    
    # Get first name
    first_name = input("First Name: ").strip()
    if not first_name:
        print("Returning to wallet menu")
        return None
        
    # Get last name
    last_name = input("Last Name: ").strip()
    if not last_name:
        print("Returning to wallet menu")
        return None
        
    # Check if name already exists
    if name_exists_in_contacts(first_name, last_name):
        print(f"\nError: A contact with the name '{first_name} {last_name}' already exists")
        print("Please use a different name")
        return None

    try:
        # Generate new wallet
        address = str(uuid4()).replace('-', '')
        
        # Create wallet with full name as nickname
        full_name = f"{first_name} {last_name}"
        wallet = {
            "address": address,
            "nickname": full_name,
            "balance": 100,
            "first_name": first_name,
            "last_name": last_name
        }
        
        # Save wallet
        wallets = load_data(WALLETS_FILE)
        wallets.append(wallet)
        save_data(wallets, WALLETS_FILE)
        
        # Create corresponding contact
        contact = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address
        }
        
        # Save contact
        contacts = load_data(CONTACTS_FILE)
        contacts.append(contact)
        save_data(contacts, CONTACTS_FILE)
        
        print(f"\nWallet created successfully!")
        print(f"Name: {full_name}")
        print(f"Address: {address}")
        print(f"Initial balance: {wallet['balance']}")
        print(f"Contact added automatically")
        
        return wallet
        
    except Exception as e:
        print(f"\nError creating wallet: {str(e)}")
        # Clean up any partial data if needed
        return None

def manage_contacts():
    while True:
        print("\n=== Contacts Management ===")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Edit Contact")
        print("\nPress Enter to return to main menu")
        
        choice = input("\nEnter choice (1-3): ").strip()
        if not choice:
            return
            
        if choice == '1':
            print("\nEnter contact details:")
            first_name = input("First Name: ").strip()
            if not first_name:
                print("Returning to contacts menu")
                continue
                
            last_name = input("Last Name: ").strip()
            if not last_name:
                print("Returning to contacts menu")
                continue
            
            # Check if name already exists
            if name_exists_in_contacts(first_name, last_name):
                print(f"\nError: A contact with the name '{first_name} {last_name}' already exists")
                continue

            contact_address = str(uuid4()).replace('-', '')
            contact = {
                "first_name": first_name,
                "last_name": last_name,
                "address": contact_address
            }
            
            contacts = load_data(CONTACTS_FILE)
            contacts.append(contact)
            save_data(contacts, CONTACTS_FILE)
            print(f"\nContact added successfully!")
            print(f"Name: {first_name} {last_name}")
            print(f"Address: {contact_address}")

        elif choice == '2':
            contacts = load_data(CONTACTS_FILE)
            if not contacts:
                print("\nNo contacts found")
                continue
                
            print("\nSaved Contacts:")
            contact_data = []
            for i, contact in enumerate(contacts, 1):
                contact_data.append([
                    str(i),
                    contact['first_name'],
                    contact['last_name'],
                    contact['address']
                ])
            
            print("\n" + tabulate(
                contact_data,
                headers=['#', 'First Name', 'Last Name', 'Address'],
                tablefmt="simple_grid"
            ))
            print()  # Add a blank line after the table

        elif choice == '3':
            contacts = load_data(CONTACTS_FILE)
            if not contacts:
                print("\nNo contacts found")
                continue
                
            print("\nSelect contact to edit:")
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact['first_name']} {contact['last_name']}")
            print("\nPress Enter to return to contacts menu")

            contact_choice = input("\nEnter contact number: ").strip()
            if not contact_choice:
                continue
                
            try:
                contact_index = int(contact_choice) - 1
                if contact_index < 0 or contact_index >= len(contacts):
                    print("Invalid contact number")
                    continue
            except ValueError:
                print("Invalid input")
                continue
                
            selected_contact = contacts[contact_index]
            
            while True:
                print(f"\nEditing: {selected_contact['first_name']} {selected_contact['last_name']}")
                print("1. Edit First Name")
                print("2. Edit Last Name")
                print("\nPress Enter to return to contacts menu")
                
                edit_choice = input("\nEnter choice (1-2): ").strip()
                if not edit_choice:
                    break
                    
                if edit_choice == '1':
                    print(f"\nCurrent first name: {selected_contact['first_name']}")
                    new_name = input("Enter new first name: ").strip()
                    if not new_name:
                        print("Returning to edit menu")
                        continue
                    selected_contact['first_name'] = new_name
                    save_data(contacts, CONTACTS_FILE)
                    print("First name updated successfully!")
                    
                elif edit_choice == '2':
                    print(f"\nCurrent last name: {selected_contact['last_name']}")
                    new_name = input("Enter new last name: ").strip()
                    if not new_name:
                        print("Returning to edit menu")
                        continue
                    selected_contact['last_name'] = new_name
                    save_data(contacts, CONTACTS_FILE)
                    print("Last name updated successfully!")
                    
                else:
                    print("Invalid choice")

def send_transaction(blockchain, current_wallet):
    while True:
        contacts = load_data(CONTACTS_FILE)
        if not contacts:
            print("\nNo contacts found. Please add a contact first.")
            return

        # Filter out the current user from the contacts list
        available_contacts = [
            contact for contact in contacts 
            if contact['address'] != current_wallet['address']
        ]

        if not available_contacts:
            print("\nNo other contacts found to send money to.")
            return

        print("\n=== Send Transaction ===")
        print(f"Your current balance: {current_wallet['balance']}")
        print("\nSelect a contact to send to:")
        
        for i, contact in enumerate(available_contacts, 1):
            print(f"{i}. {contact['first_name']} {contact['last_name']}")
        print("\nPress Enter to return to main menu")

        contact_choice = input("\nEnter contact number: ").strip()
        if not contact_choice:
            return
            
        try:
            contact_index = int(contact_choice) - 1
            if contact_index < 0 or contact_index >= len(available_contacts):
                print("Invalid contact number")
                continue
        except ValueError:
            print("Invalid input")
            continue

        selected_contact = available_contacts[contact_index]

        amount = input("\nEnter amount: ").strip()
        if not amount:
            print("Returning to send menu")
            continue
            
        try:
            amount = float(amount)
            if amount <= 0:
                print("Amount must be positive")
                continue
            if amount > current_wallet['balance']:
                print(f"\nInsufficient funds! Your balance is {current_wallet['balance']}")
                continue
        except ValueError:
            print("Invalid amount")
            continue

        confirm = input(f"\nSend {amount} to {selected_contact['first_name']} {selected_contact['last_name']}? (y/n): ").lower()
        if confirm != 'y':
            print("Transaction cancelled")
            continue

        # Create and record the transaction
        transaction = blockchain.create_transaction(
            current_wallet['address'],
            selected_contact['address'],
            amount
        )
        
        # Update wallet balances
        update_wallet_balance(current_wallet['address'], -amount)  # Deduct from sender
        update_wallet_balance(selected_contact['address'], amount)  # Add to receiver
        
        # Update the current_wallet object to reflect new balance
        current_wallet['balance'] -= amount
        
        # Record the transaction
        record_transaction(transaction, current_wallet['address'], "sent")
        print("\nTransaction created and added to pending transactions!")
        print(f"Your new balance: {current_wallet['balance']}")

def view_transaction_history():
    while True:
        print("\n=== Transaction History ===")
        print("1. View All Transactions")
        print("2. View Transactions with Contact")
        print("\nPress Enter to return to main menu")
        
        choice = input("\nEnter choice (1-2): ").strip()
        if not choice:
            return
            
        if choice == '1':
            transactions = load_data(COMPLETED_TRANSACTIONS_FILE)
            if not transactions:
                print("\nNo transactions found")
                continue
                    
            # Load contacts and wallets for display
            contacts = load_data(CONTACTS_FILE)
            wallets = load_data(WALLETS_FILE)
            
            # Prepare headers with exact widths
            headers = [
                pad_to_width('Type', 12),
                pad_to_width('Amount', 14),
                pad_to_width('From', 50),
                pad_to_width('To', 50),
                pad_to_width('Time', 21)
            ]
            
            # Ensure all data rows have exact widths
            tx_data = []
            for tx in transactions:
                tx_data.append([
                    format_type(tx['type'].upper()),
                    format_amount(tx['amount']),
                    format_address_with_name(tx['sender'], contacts, wallets, is_sender=True),
                    format_address_with_name(tx['receiver'], contacts, wallets, is_sender=False),
                    format_timestamp(tx['timestamp'])
                ])
            
            print("\n" + tabulate(
                tx_data,
                headers=headers,
                tablefmt="simple_grid",
                colalign=("center", "center", "center", "center", "center"),
                disable_numparse=True))

        elif choice == '2':
            contacts = load_data(CONTACTS_FILE)
            if not contacts:
                print("\nNo contacts found")
                continue
                
            print("\nSelect contact to view transactions (or press Enter to cancel):")
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact['first_name']} {contact['last_name']}")

            contact_choice = input("\nEnter contact number: ").strip()
            if not contact_choice:
                print("Cancelled - Returning to previous menu")
                continue
                
            try:
                contact_index = int(contact_choice) - 1
                if contact_index < 0 or contact_index >= len(contacts):
                    print("Invalid contact number")
                    continue
            except ValueError:
                print("Invalid input")
                continue
                
            selected_contact = contacts[contact_index]
            tx_file = get_transaction_file(selected_contact['address'])
            transactions = load_data(tx_file)
            
            print(f"\nTransactions for {selected_contact['first_name']} {selected_contact['last_name']}:")
            if not transactions:
                print(" No transactions found")
            else:
                for tx in transactions:
                    print(f"\n{time.ctime(tx['timestamp'])} - {tx['type'].upper()}: {tx['amount']} coins")
                    print(f" From: {tx['sender']}")
                    print(f" To: {tx['receiver']}")

def format_address(addr, width=36):
    """Format address to fixed width, centered"""
    return pad_to_width(addr, width)

def format_address_with_name(addr, contacts, wallets, is_sender=False, width=50):
    """Format address with contact name or wallet nickname if available"""
    display_name = None
    
    if is_sender:
        # For senders, check wallets first
        for wallet in wallets:
            if wallet['address'] == addr:
                display_name = wallet['nickname']
                break
    
    # If no wallet nickname found (or is receiver), check contacts
    if not display_name:
        for contact in contacts:
            if contact['address'] == addr:
                display_name = contact['first_name'] + ' ' + contact['last_name']
                break
    
    if display_name:
        display = f"{addr} ({display_name})"
    else:
        display = addr
    
    return pad_to_width(display, width)

def format_amount(amount, width=14):
    """Format amount to fixed width, centered"""
    return pad_to_width(str(amount), width)

def format_timestamp(ts, width=21):
    """Format timestamp to fixed width, centered"""
    time_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return pad_to_width(time_str, width)

def format_type(tx_type, width=12):
    """Format transaction type, centered"""
    return pad_to_width(tx_type, width)

def format_hash(hash_value, width=66):
    """Format hash to fixed width"""
    return hash_value.center(width)

def main_menu():
    blockchain = Blockchain()
    current_wallet = None

    while True:
        # Wallet selection/creation
        if not current_wallet:
            wallet = select_wallet()
            if not wallet:
                print("\nPlease select or create a wallet to continue")
                continue
            current_wallet = wallet

        # Display current user info
        print("\n" + "="*50)
        # Handle both old and new wallet formats
        if 'first_name' in current_wallet and 'last_name' in current_wallet:
            user_name = f"{current_wallet['first_name']} {current_wallet['last_name']}"
        else:
            user_name = current_wallet['nickname']
        print(f"Current User: {user_name}")
        print(f"Balance: {current_wallet['balance']}")
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
                if not current_wallet:
                    print("\n Please select or create a wallet first!")
                    continue

                contacts = load_data(CONTACTS_FILE)
                if not contacts:
                    print("\n No contacts available! Please add contacts first.")
                    continue

                send_transaction(blockchain, current_wallet)

            elif choice == '2':
                if not current_wallet:
                    print("\n Please select or create a wallet first!")
                    continue

                print("\nMining pending transactions...")
                pending_count = len(blockchain.pending_transactions)
                
                if pending_count == 0:
                    print("No transactions available for mining.")
                    print("Press Enter to return to main menu")
                    input()
                    continue
                    
                print(f"Pending transactions: {pending_count}")
                confirm = input("\nStart mining? (press Enter to cancel): ").strip()
                if not confirm:
                    print("Mining cancelled - Returning to main menu")
                    continue
                
                try:
                    processed_count = blockchain.mine_pending_transactions(current_wallet['address'])
                    print(f"\nBlock mined successfully! {processed_count} transactions processed.")
                    print(f"Mining reward: {blockchain.mining_reward} coins added to your wallet")
                    reward_tx = {
                        "id": str(uuid4()),
                        "sender": "Network Reward",
                        "receiver": current_wallet['address'],
                        "amount": blockchain.mining_reward,
                        "timestamp": time.time()
                    }
                    record_transaction(reward_tx, current_wallet['address'], "Network Reward")
                except ValueError as e:
                    print(f"\nMining failed: {str(e)}")
                except Exception as e:
                    print(f"\nMining failed: {str(e)}")

            elif choice == '3':
                print("\n=== Blockchain Info ===")
                print(f" Chain length: {len(blockchain.chain)} blocks")
                print(f" Pending transactions: {len(blockchain.pending_transactions)}")
                print(f" Chain validity: {'Valid' if blockchain.validate_chain() else 'Invalid'}")

                if input("\nView block details? (press Enter to skip): ").strip():
                    for i, block in enumerate(blockchain.chain):
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
                                contacts = load_data(CONTACTS_FILE)
                                wallets = load_data(WALLETS_FILE)
                                
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

            elif choice == '4':
                if not current_wallet:
                    print("\n No wallet selected!")
                    continue

                tx_file = get_transaction_file(current_wallet['address'])
                transactions = load_data(tx_file)
                print(f"\n Transaction History for {current_wallet['nickname']}")
                print("=" * 50)
                
                if not transactions:
                    print("\n No transactions found")
                else:
                    # Load contacts and wallets for display
                    contacts = load_data(CONTACTS_FILE)
                    wallets = load_data(WALLETS_FILE)
                    
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
                        tx_type = tx['type'].upper()
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

            elif choice == '5':
                contacts = load_data(CONTACTS_FILE)
                if not contacts:
                    print("\nNo contacts available!")
                    continue

                print("\nSelect Contact:")
                for i, contact in enumerate(contacts, 1):
                    print(f"{i}. {contact['first_name']} {contact['last_name']}")

                try:
                    contact_index = int(input("\nEnter contact number: ")) - 1
                    if 0 <= contact_index < len(contacts):
                        contact = contacts[contact_index]
                        tx_file = get_transaction_file(contact['address'])
                        transactions = load_data(tx_file)
                        
                        print(f"\nTransactions for {contact['first_name']} {contact['last_name']}:")
                        if not transactions:
                            print(" No transactions found")
                        else:
                            for tx in transactions:
                                print(f"\n{time.ctime(tx['timestamp'])} - {tx['type'].upper()}: {tx['amount']} coins")
                                print(f" From: {tx['sender']}")
                                print(f" To: {tx['receiver']}")
                    else:
                        print(" Invalid contact selection")
                except ValueError:
                    print(" Please enter a valid number")

            elif choice == '6':
                manage_contacts()

            elif choice == '7':
                current_wallet = select_wallet()

            elif choice == '8':
                print("\n Exiting...")
                break

            else:
                print("\n Invalid choice")

        except Exception as e:
            print(f"\n Error: {str(e)}")

if __name__ == "__main__":
    main_menu()

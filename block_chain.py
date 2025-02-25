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
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.mining_reward = 10
        self.load_pending_transactions()

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
            return False

        # Create mining reward transaction
        reward_transaction = {
            'sender': "0",  # 0 indicates system reward
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

        # Update completed transactions
        completed_transactions = load_data(COMPLETED_TRANSACTIONS_FILE)
        completed_transactions.extend(pending_transactions + [reward_transaction])
        save_data(completed_transactions, COMPLETED_TRANSACTIONS_FILE)

        # Clear pending transactions
        save_data([], PENDING_TRANSACTIONS_FILE)

        # Update miner's wallet with reward
        update_wallet_balance(miner_address, self.mining_reward)

        return True

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

def record_transaction(transaction, wallet_address, transaction_type):
    tx_file = get_transaction_file(wallet_address)
    transactions = load_data(tx_file)
    transactions.append({
        **transaction,
        "type": transaction_type,
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

def create_wallet():
    """Create a new wallet and corresponding contact"""
    first_name = get_valid_input(
        "First Name: ",
        lambda x: len(x) > 0,
        "First name cannot be empty"
    )
    last_name = get_valid_input(
        "Last Name: ",
        lambda x: len(x) > 0,
        "Last name cannot be empty"
    )
    
    full_name = f"{first_name} {last_name}"
    address = str(uuid4()).replace('-', '')
    
    # Create wallet
    wallet = {
        "address": address,
        "nickname": full_name,
        "balance": 100
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
    print(f"Address: {address}")
    print(f"Initial balance: {wallet['balance']}")
    print(f"Contact added: {full_name}")
    return wallet

def select_wallet():
    wallets = load_data(WALLETS_FILE)
    if not wallets:
        print(" No wallets found!")
        return None
    print("\nSaved Wallets:")
    for i, wallet in enumerate(wallets, 1):
        print(f"{i}. {wallet['nickname']} ({wallet['address']})")
    while True:
        choice = input("\nSelect wallet (number) or 'new' to create: ")
        if choice.lower() == 'new':
            return None
        try:
            index = int(choice) - 1
            if 0 <= index < len(wallets):
                return wallets[index]
            print(" Invalid selection")
        except ValueError:
            print(" Please enter a valid number")

def manage_contacts():
    while True:
        print("\n=== Contacts Management ===")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Back to Main Menu")
        
        choice = input("\nEnter choice (1-3): ")
        
        if choice == '3':
            return
        
        if choice == '1':
            print("\nEnter contact details (or press Enter to cancel):")
            first_name = input("First Name: ").strip()
            if not first_name:
                print("Cancelled - Returning to contacts menu")
                continue
                
            last_name = input("Last Name: ").strip()
            if not last_name:
                print("Cancelled - Returning to contacts menu")
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
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact['first_name']} {contact['last_name']}")
                print(f"   Address: {contact['address']}\n")

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
        print(f"{len(available_contacts) + 1}. Back to Main Menu")

        contact_choice = input("\nEnter choice: ")
        if contact_choice == str(len(available_contacts) + 1):
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

        amount = input("\nEnter amount (or press Enter to cancel): ").strip()
        if not amount:
            print("Cancelled - Returning to send menu")
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
        print("3. Back to Main Menu")
        
        choice = input("\nEnter choice (1-3): ")
        
        if choice == '3':
            return
            
        if choice == '1':
            transactions = load_data(COMPLETED_TRANSACTIONS_FILE)
            if not transactions:
                print("\nNo transactions found")
                continue

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
    """Format transaction type with emoji, centered"""
    type_emoji = {
        'SENT': '📤',
        'RECEIVED': '📥',
        'REWARD': '🎁'
    }.get(tx_type, '💱')
    formatted = f"{type_emoji} {tx_type}"
    return pad_to_width(formatted, width + 2)  # +2 for emoji width

def format_hash(hash_value, width=66):
    """Format hash to fixed width"""
    return hash_value.center(width)

def main_menu():
    blockchain = Blockchain()
    current_wallet = None

    # Wallet selection
    wallet = select_wallet()
    if wallet:
        current_wallet = wallet
        print(f"\nLogged in as: {wallet['nickname']}")
    else:
        current_wallet = create_wallet()

    while True:
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

                print("\n=== Mining ===")
                if not blockchain.pending_transactions:
                    print(" No pending transactions to mine")
                    continue

                print(f" Pending transactions: {len(blockchain.pending_transactions)}")
                confirm = input("\nStart mining? This may take time (y/n): ").lower()
                if confirm == 'y':
                    try:
                        mined_count = blockchain.mine_pending_transactions(current_wallet['address'])
                        print(f"\n Block mined successfully! {mined_count} transactions processed.")
                        print(f" Mining reward: {blockchain.mining_reward} coins added to your wallet")
                        reward_tx = {
                            "id": str(uuid4()),
                            "sender": "network",
                            "receiver": current_wallet['address'],
                            "amount": blockchain.mining_reward,
                            "timestamp": time.time()
                        }
                        record_transaction(reward_tx, current_wallet['address'], "reward")
                    except ValueError as e:
                        print(f"\n Mining failed: {str(e)}")
                    except Exception as e:
                        print(f"\n Mining failed: {str(e)}")
                else:
                    print("\n Mining canceled")

            elif choice == '3':
                print("\n=== Blockchain Info ===")
                print(f" Chain length: {len(blockchain.chain)} blocks")
                print(f" Pending transactions: {len(blockchain.pending_transactions)}")
                print(f" Chain validity: {'Valid' if blockchain.validate_chain() else 'Invalid'}")

                if input("\nView block details? (y/n): ").lower() == 'y':
                    for i, block in enumerate(blockchain.chain):
                        print(f"\n📦 Block #{i}")
                        print("=" * 50)
                        
                        # Basic block info
                        block_info = [
                            ["Index", str(block.index).center(10)],
                            ["Timestamp", format_timestamp(block.timestamp)],
                            ["Previous Hash", format_hash(block.previous_hash)],
                            ["Hash", format_hash(block.hash)],
                            ["Nonce", str(block.nonce).center(10)]
                        ]
                        print(tabulate(block_info, tablefmt="fancy_grid"))
                        
                        # If it's not the genesis block, show transactions
                        if isinstance(block.transactions, list):
                            print("\n📝 Transactions in this block:")
                            tx_data = []
                            for tx in block.transactions:
                                tx_data.append([
                                    format_address(tx['sender']),
                                    format_address(tx['receiver']),
                                    format_amount(tx['amount']),
                                    format_timestamp(tx['timestamp'])
                                ])
                            if tx_data:
                                print(tabulate(tx_data, 
                                            headers=['From'.center(36), 'To'.center(36), 
                                                    'Amount'.center(14), 'Time'.center(21)],
                                            tablefmt="fancy_grid"))
                            else:
                                print("No transactions in this block")
                        print("\n")

            elif choice == '4':
                if not current_wallet:
                    print("\n No wallet selected!")
                    continue

                tx_file = get_transaction_file(current_wallet['address'])
                transactions = load_data(tx_file)
                print(f"\n💼 Transaction History for {current_wallet['nickname']}")
                print("=" * 50)
                
                if not transactions:
                    print("\n No transactions found")
                else:
                    # Load contacts and wallets for display
                    contacts = load_data(CONTACTS_FILE)
                    wallets = load_data(WALLETS_FILE)
                    
                    # Prepare headers with exact widths
                    headers = [
                        pad_to_width('Type', 14),      # 12 + 2 for emoji
                        pad_to_width('Amount', 14),
                        pad_to_width('From', 50),      # Increased width for names
                        pad_to_width('To', 50),        # Increased width for names
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
                                 tablefmt="simple",
                                 colalign=("center", "center", "center", "center", "center"),
                                 disable_numparse=True) + "\n")

            elif choice == '5':
                contacts = load_data(CONTACTS_FILE)
                if not contacts:
                    print("\n No contacts available!")
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

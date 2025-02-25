import hashlib
import json
import os
import time
from uuid import uuid4

# File paths
WALLETS_FILE = "wallets.json"
CONTACTS_FILE = "contacts.json"
TRANSACTIONS_DIR = "transactions"

os.makedirs(TRANSACTIONS_DIR, exist_ok=True)

def get_valid_input(prompt, validation_func, error_message):
    while True:
        value = input(prompt).strip()
        if validation_func(value):
            return value
        print(error_message)

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
        self.pending_transactions = []
        self.difficulty = 4
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def create_transaction(self, sender, receiver, amount):
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": time.time()
        }
        self.pending_transactions.append(transaction)
        return transaction

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            raise ValueError("No transactions to mine")
        
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=self.get_last_block().hash
        )
        block.nonce = self.proof_of_work(block)
        block.hash = block.calculate_hash()
        self.chain.append(block)
        self.pending_transactions = []
        self.create_transaction("network", miner_address, self.mining_reward)

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

def create_wallet(nickname):
    wallet = {
        "address": str(uuid4()).replace('-', ''),
        "nickname": nickname,
        "created_at": time.time()
    }
    wallets = load_data(WALLETS_FILE)
    wallets.append(wallet)
    save_data(wallets, WALLETS_FILE)
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
    contacts = load_data(CONTACTS_FILE)
    while True:
        print("\nContact Management:")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Delete Contact")
        print("4. Return to Main Menu")
        choice = input("Choose option: ")

        if choice == '1':
            contact_address = str(uuid4()).replace('-', '')
            contact = {
                "first_name": get_valid_input(
                    "First Name: ",
                    lambda x: len(x) > 0,
                    "First name cannot be empty"
                ),
                "last_name": get_valid_input(
                    "Last Name: ",
                    lambda x: len(x) > 0,
                    "Last name cannot be empty"
                ),
                "address": contact_address
            }
            contacts.append(contact)
            save_data(contacts, CONTACTS_FILE)
            print(f"\nContact added with address: {contact_address}")

        elif choice == '2':
            if not contacts:
                print("\n No contacts found!")
                continue
            print("\nSaved Contacts:")
            for i, contact in enumerate(contacts, 1):
                print(f"{i}. {contact['first_name']} {contact['last_name']}")
                print(f"   Address: {contact['address']}\n")

        elif choice == '3':
            if not contacts:
                print("\n No contacts to delete!")
                continue
            try:
                index = int(input("Enter contact number to delete: ")) - 1
                if 0 <= index < len(contacts):
                    del contacts[index]
                    save_data(contacts, CONTACTS_FILE)
                    print(" Contact deleted")
                else:
                    print(" Invalid index")
            except ValueError:
                print(" Please enter a valid number")

        elif choice == '4':
            break

        else:
            print(" Invalid choice")

def main_menu():
    blockchain = Blockchain()
    current_wallet = None

    # Wallet selection
    wallet = select_wallet()
    if wallet:
        current_wallet = wallet
        print(f"\nLogged in as: {wallet['nickname']}")
    else:
        nickname = get_valid_input(
            "Enter wallet nickname: ",
            lambda x: len(x) > 0,
            "Nickname cannot be empty"
        )
        current_wallet = create_wallet(nickname)
        print(f"\nNew wallet created: {current_wallet['address']}")

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

                print("\nSelect Contact to Send To:")
                for i, contact in enumerate(contacts, 1):
                    print(f"{i}. {contact['first_name']} {contact['last_name']}")

                contact_index = int(get_valid_input(
                    "\nEnter contact number: ",
                    lambda x: x.isdigit() and 1 <= int(x) <= len(contacts),
                    f" Please enter a number between 1-{len(contacts)}"
                )) - 1

                selected_contact = contacts[contact_index]
                receiver_address = selected_contact['address']

                amount = float(get_valid_input(
                    "\nAmount to send: ",
                    lambda x: x.replace('.', '', 1).isdigit() and float(x) > 0,
                    " Invalid amount (must be positive number)"
                ))

                confirm = input(f"\nSend {amount} to {selected_contact['first_name']} {selected_contact['last_name']}? (y/n): ").lower()
                if confirm == 'y':
                    transaction = blockchain.create_transaction(
                        current_wallet['address'],
                        receiver_address,
                        amount
                    )
                    record_transaction(transaction, current_wallet['address'], "sent")
                    print("\n Transaction created!")
                else:
                    print("\n Transaction canceled")

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
                        blockchain.mine_pending_transactions(current_wallet['address'])
                        print("\n Block mined successfully!")
                        print(f" Mining reward: {blockchain.mining_reward} coins added to your wallet")
                        reward_tx = {
                            "sender": "network",
                            "receiver": current_wallet['address'],
                            "amount": blockchain.mining_reward,
                            "timestamp": time.time()
                        }
                        record_transaction(reward_tx, current_wallet['address'], "reward")
                    except Exception as e:
                        print(f"\n Mining failed: {str(e)}")
                else:
                    print("\n Mining canceled")

            elif choice == '3':
                print("\n=== Blockchain Info ===")
                print(f" Chain length: {len(blockchain.chain)} blocks")
                print(f" Pending transactions: {len(blockchain.pending_transactions)}")
                print(f" Chain validity: {'Valid' if blockchain.validate_chain() else 'Invalid'}")

                if input("\nView details? (y/n): ").lower() == 'y':
                    for block in blockchain.chain:
                        print("\n" + "-"*50)
                        print(block)

            elif choice == '4':
                if not current_wallet:
                    print("\n No wallet selected!")
                    continue

                tx_file = get_transaction_file(current_wallet['address'])
                transactions = load_data(tx_file)
                print(f"\nTransaction history for {current_wallet['nickname']}:")
                
                if not transactions:
                    print(" No transactions found")
                else:
                    for tx in transactions:
                        print(f"\n{time.ctime(tx['timestamp'])} - {tx['type'].upper()}: {tx['amount']} coins")
                        print(f" From: {tx['sender']}")
                        print(f" To: {tx['receiver']}")

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
import hashlib
import json
import time
from uuid import uuid4

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
        self.pending_transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": time.time()
        })

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

def create_wallet():
    return str(uuid4()).replace('-', '')

def get_valid_input(prompt, validation_func, error_message):
    while True:
        try:
            value = input(prompt).strip()
            if validation_func(value):
                return value
            print(error_message)
        except Exception as e:
            print(f"Invalid input: {str(e)}")

def main_menu():
    blockchain = Blockchain()
    current_wallet = None
    
    while True:
        print("\n=== Blockchain Interactive Menu ===")
        print("1. Create New Wallet")
        print("2. Send Transaction")
        print("3. Mine Pending Transactions")
        print("4. View Blockchain")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        try:
            if choice == '1':
                current_wallet = create_wallet()
                print(f"\nNew wallet created successfully!")
                print(f"Your wallet address: {current_wallet}")
                
            elif choice == '2':
                if not current_wallet:
                    print("\nPlease create a wallet first!")
                    continue
                
                print("\n=== New Transaction ===")
                receiver = get_valid_input(
                    "Receiver's address: ",
                    lambda x: len(x) == 32 and x.isalnum(),
                    "Invalid address format (must be 32 alphanumeric characters)"
                )
                
                amount = float(get_valid_input(
                    "Amount to send: ",
                    lambda x: x.replace('.', '', 1).isdigit() and float(x) > 0,
                    "Invalid amount (must be positive number)"
                ))
                
                confirm = input(f"\nSend {amount} coins to {receiver}? (y/n): ").lower()
                if confirm == 'y':
                    blockchain.create_transaction(current_wallet, receiver, amount)
                    print("\nTransaction added to pending transactions!")
                else:
                    print("\nTransaction canceled")
                    
            elif choice == '3':
                if not current_wallet:
                    print("\nPlease create a wallet first!")
                    continue
                
                print("\n=== Mining ===")
                print(f"Pending transactions: {len(blockchain.pending_transactions)}")
                if not blockchain.pending_transactions:
                    print("No pending transactions to mine")
                    continue
                
                confirm = input("Start mining? This may take time (y/n): ").lower()
                if confirm == 'y':
                    try:
                        blockchain.mine_pending_transactions(current_wallet)
                        print("\nBlock mined successfully!")
                        print(f"Mining reward: {blockchain.mining_reward} coins added to your wallet")
                    except Exception as e:
                        print(f"\nMining failed: {str(e)}")
                else:
                    print("\nMining canceled")
                    
            elif choice == '4':
                print("\n=== Blockchain Explorer ===")
                print(f"Chain length: {len(blockchain.chain)} blocks")
                print(f"Pending transactions: {len(blockchain.pending_transactions)}")
                print(f"Chain validity: {'Valid' if blockchain.validate_chain() else 'Invalid'}")
                
                view_details = input("\nView detailed blocks? (y/n): ").lower()
                if view_details == 'y':
                    for block in blockchain.chain:
                        print("\n" + "-"*50)
                        print(block)
                        
            elif choice == '5':
                print("\nExiting blockchain system...")
                break
                
            else:
                print("\nInvalid choice. Please enter a number between 1-5")
                
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Returning to main menu...")

if __name__ == "__main__":
    main_menu()
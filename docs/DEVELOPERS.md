# 👩‍💻 Blockchain Wallet Developer Guide

## 🏗️ Project Structure
```
blockchain_project/
├── block_chain.py     # Main application file
├── wallets.json       # Wallet storage
├── contacts.json      # Contact information
├── blockchain.json    # Blockchain data
├── pending_transactions.json # Unconfirmed transactions
├── completed_transactions.json # Processed transactions
├── transactions/      # Transaction history
│   └── transactions_[wallet_address].json
├── docs/
│   ├── USERS.md      # User documentation
│   └── DEVELOPERS.md # Developer documentation
└── README.md         # Project overview
```

## 💻 Core Components

### Block Class
- Manages individual blocks in the chain
- Handles block hashing and validation
- Properties:
  - index
  - timestamp
  - transactions
  - previous_hash
  - nonce

### Blockchain Class
- Manages the entire blockchain
- Handles:
  - Chain initialization
  - Transaction creation
  - Block mining
  - Chain validation
- Properties:
  - chain
  - pending_transactions
  - mining_reward

### File Management
- `wallets.json`: Stores wallet information and balances
- `contacts.json`: Stores contact details
- `blockchain.json`: Stores the entire blockchain data
- `pending_transactions.json`: Temporary storage for unconfirmed transactions
- `completed_transactions.json`: Archive of all processed transactions
- `transactions/`: Directory for per-wallet transaction histories

## 🧪 Testing
To implement tests:
1. Create test cases for:
   - Block creation and validation
   - Transaction processing
   - Mining operations
   - File operations
2. Test edge cases:
   - Invalid transactions
   - Chain validation
   - Concurrent operations

## 🐛 Debugging
Debug points to consider:
1. Transaction validation
2. Block mining process
3. File operations
4. User input validation

## 🔄 Workflow
1. **Initialization**
   - Load existing data
   - Create necessary directories
   - Initialize blockchain

2. **Transaction Flow**
   - Create transaction
   - Validate transaction
   - Add to pending transactions
   - Mine block
   - Update transaction history

3. **Mining Process**
   - Collect pending transactions
   - Create new block
   - Calculate proof of work
   - Add block to chain
   - Clear pending transactions

## 🛠️ Development Setup
1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies (if any)
4. Run the application:
   ```bash
   python block_chain.py
   ```

## 📈 Future Improvements
1. Add network capabilities
2. Implement public/private key cryptography
3. Add transaction fees
4. Improve mining algorithm
5. Add block explorer UI
6. Implement wallet backup/restore
7. Add multi-signature transactions
8. Implement smart contracts
9. Add support for multiple cryptocurrencies
10. Enhance transaction privacy features

## 🤝 Contributing Guidelines
1. Fork the repository
2. Create feature branch
3. Follow code style guidelines
4. Write clear commit messages
5. Submit pull request

## 📚 API Documentation

### Block Methods
```python
def calculate_hash(self)
def __str__(self)
```

### Blockchain Methods
```python
def create_genesis_block(self)
def get_latest_block(self)
def create_transaction(self, sender, receiver, amount)
def mine_pending_transactions(self, miner_address)
def get_balance(self, address)
def validate_chain(self)
```

### Utility Functions
```python
def load_data(file_path)
def save_data(data, file_path)
def get_transaction_file(wallet_address)
def record_transaction(transaction, wallet_address, tx_type)
def update_wallet_balance(address, amount_change)
def name_exists_in_contacts(first_name, last_name)
def format_address(addr, width=36)
def format_address_with_name(addr, contacts, wallets, is_sender=False, width=50)
def format_amount(amount, width=14)
def format_timestamp(ts, width=21)
def format_type(tx_type, width=12)
def format_hash(hash_value, width=66)
def get_string_width(s)
def pad_to_width(s, width)
```

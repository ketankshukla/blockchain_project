# 👩‍💻 Developer Documentation

<div style="background-color: #e6f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #1890ff;">

This document provides technical information about the blockchain application architecture, how to set up the development environment, and how to extend the application.

</div>

## 🏗️ Project Structure

<div style="background-color: #fff7e6; padding: 15px; border-radius: 8px; border-left: 5px solid #fa8c16;">

The application is organized into the following modules:

```
refactored/
├── blockchain/            # Core blockchain implementation
│   ├── __init__.py
│   ├── block.py           # Block class definition
│   ├── transaction.py     # Transaction class definition
│   └── blockchain.py      # Blockchain class implementation
├── data/                  # Data storage and management
│   ├── __init__.py
│   └── data_handler.py    # JSON file handling
├── ui/                    # User interface components
│   ├── __init__.py
│   ├── wallet_ui.py       # Wallet management interface
│   ├── transaction_ui.py  # Transaction interface
│   ├── blockchain_ui.py   # Blockchain viewing interface
│   └── contacts_ui.py     # Contact management interface
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── formatting.py      # Text formatting utilities
│   └── validation.py      # Input validation utilities
├── docs/                  # Documentation
│   ├── DEVELOPERS.md      # This file
│   └── USERS.md           # User guide
├── main.py                # Application entry point
└── README.md              # Project overview
```

</div>

## 🚀 Development Setup

<div style="background-color: #f6ffed; padding: 15px; border-radius: 8px; border-left: 5px solid #52c41a;">

### Prerequisites

- Python 3.8 or higher
- `tabulate` package for formatting tabular data

### Environment Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   # On Windows
   .\.venv\Scripts\activate.bat
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application for Development

You can run the application using Python:

```bash
python main.py
```

### Python Import Structure

The application uses absolute imports to avoid path-related issues. The main.py file includes:

```python
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

This ensures that modules can be imported correctly regardless of the directory from which you run the application.

</div>

## 📦 Core Components

<div style="background-color: #f9f0ff; padding: 15px; border-radius: 8px; border-left: 5px solid #722ed1;">

### 🧱 Block

The `Block` class (`blockchain/block.py`) represents a single block in the blockchain.

```python
# Key methods:
calculate_hash()  # Computes the SHA-256 hash of the block's contents
```

### 💰 Transaction

The `Transaction` class (`blockchain/transaction.py`) represents a transfer of coins between wallets.

```python
# Key methods:
to_dict()      # Converts transaction to a dictionary for storage
from_dict()    # Creates a Transaction object from a dictionary
```

### ⛓️ Blockchain

The `Blockchain` class (`blockchain/blockchain.py`) manages the chain of blocks and operations.

```python
# Key methods:
create_transaction()        # Creates a new transaction
mine_pending_transactions() # Mines a new block with pending transactions
validate_chain()            # Validates the integrity of the blockchain
```

### 💾 Data Handler

The `DataHandler` class (`data/data_handler.py`) provides storage operations.

```python
# Key methods:
load_blockchain()           # Loads blockchain data from storage
save_blockchain()           # Saves blockchain data to storage
update_wallet_balance()     # Updates a wallet's balance
record_transaction()        # Records a transaction in a wallet's history
```

</div>

## 🧪 Testing

<div style="background-color: #e6f7ff; padding: 15px; border-radius: 8px; border-left: 5px solid #1890ff;">

### Manual Testing

Test the application by running it and performing various operations:

```bash
python main.py
```

Common test scenarios:
1. Create a new wallet
2. Send a transaction between wallets
3. Mine a block
4. View transaction history
5. Check blockchain validity

### Unit Testing

A future enhancement would be to add unit tests for each component.

</div>

## 🔄 Workflow

<div style="background-color: #fff2e8; padding: 15px; border-radius: 8px; border-left: 5px solid #fa541c;">

### Adding a New Feature

1. Identify which module should contain the feature
2. Implement the feature in the appropriate class
3. Update the UI to expose the feature
4. Update documentation

### Modifying Existing Features

1. Locate the relevant files
2. Make changes ensuring backward compatibility
3. Test the feature thoroughly
4. Update documentation

</div>

## 🐛 Debugging and Troubleshooting

<div style="background-color: #fff2e8; padding: 15px; border-radius: 8px; border-left: 5px solid #fa541c;">

### Common Issues

- **ImportError**: Ensure the Python path is correctly set up (see "Python Import Structure" above).
- **File not found errors**: Check that all JSON files exist in the expected locations.
- **Transaction validation issues**: Verify wallet balances and transaction logic.
- **Blockchain validation failures**: Check hash calculation and chain integrity.
- **NoneType errors in transaction display**: The application now handles null transaction types gracefully.

### Debug Strategies

- Add print statements to track execution flow
- Review JSON files to check data integrity
- Verify class initialization parameters

</div>

## 🚧 Extending the Application

<div style="background-color: #fcffe6; padding: 15px; border-radius: 8px; border-left: 5px solid #a0d911;">

### Adding a New UI Interface

The business logic is separated from the UI, making it easy to add new interfaces:

1. Create a new module for your interface (e.g., `web_ui/`)
2. Import the blockchain and data components
3. Implement your interface using the existing methods

### Adding New Blockchain Features

To add new blockchain features like smart contracts:

1. Extend the `Blockchain` class with new methods
2. Update the `Block` or `Transaction` classes if needed
3. Add UI components to expose the new features

</div>

## 🤝 Contributing

<div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 5px solid #434343;">

### Contribution Guidelines

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request with a clear description of changes

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions and methods
- Document new functions and classes with docstrings
- Keep code modular and maintainable

</div>

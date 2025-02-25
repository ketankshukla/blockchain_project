# 🔄 Function Call Flows

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #4285f4;">

This document provides detailed information about the function call flows in the blockchain application. It maps out the sequence of function calls as you navigate through different menus and perform various actions.

</div>

## 📋 Table of Contents

- [Application Startup Flow](#application-startup-flow)
- [Main Menu Navigation](#main-menu-navigation)
- [Transaction Flows](#transaction-flows)
- [Blockchain Flows](#blockchain-flows)
- [Wallet Management Flows](#wallet-management-flows)
- [Contact Management Flows](#contact-management-flows)
- [Function Call Diagrams](#function-call-diagrams)

## 🚀 Application Startup Flow

<div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 5px solid #4caf50;">

The application startup sequence follows these function calls:

1. `main.py` → `__main__` block
2. `main.py` → `BlockchainApp.__init__()`
   - `DataHandler.__init__()`
   - `Blockchain.__init__()`
   - `WalletUI.__init__()`
   - `TransactionUI.__init__()`
   - `BlockchainUI.__init__()`
   - `ContactsUI.__init__()`
3. `main.py` → `BlockchainApp.run()`
   - Initial menu display (continue or exit)
   - If continue:
     - `WalletUI.select_wallet()`
   - Main menu display

Exiting from startup:
- `BlockchainApp.run()` → `sys.exit(0)` (when selecting option 2)

</div>

## 🧭 Main Menu Navigation

<div style="background-color: #fff8e1; padding: 15px; border-radius: 8px; border-left: 5px solid #ffb300;">

The main menu provides access to all features. Here's how the function calls flow from the main menu:

### From Main Menu to Feature:

1. **Send Transaction (Option 1)**:
   - `BlockchainApp.run()` → `TransactionUI.send_transaction()`

2. **Mine Transactions (Option 2)**:
   - `BlockchainApp.run()` → `BlockchainUI.mine_transactions()`

3. **View Blockchain (Option 3)**:
   - `BlockchainApp.run()` → `BlockchainUI.view_blockchain()`

4. **View My Transactions (Option 4)**:
   - `BlockchainApp.run()` → `TransactionUI.view_transaction_history()`

5. **View Contact Transactions (Option 5)**:
   - `BlockchainApp.run()` → `TransactionUI.view_contact_transactions()`

6. **Manage Contacts (Option 6)**:
   - `BlockchainApp.run()` → `ContactsUI.manage_contacts()`

7. **Switch Wallet (Option 7)**:
   - `BlockchainApp.run()` → `WalletUI.select_wallet()`

8. **Exit (Option 8)**:
   - `BlockchainApp.run()` → `sys.exit(0)`

### Returning to Main Menu:

- Most features have built-in return mechanisms:
  - User input prompts (press Enter to return)
  - Explicit return options
  - Function completion naturally returns to the main menu loop

</div>

## 💸 Transaction Flows

<div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 5px solid #2196f3;">

### Send Transaction Flow:

1. `BlockchainApp.run()` → `TransactionUI.send_transaction()`
   - `DataHandler.load_contacts()`
   - User selects recipient
   - User enters amount
   - User confirms transaction
   - `Blockchain.create_transaction()`
   - `DataHandler.update_wallet_balance()` (sender)
   - `DataHandler.update_wallet_balance()` (recipient)
   - `DataHandler.record_transaction()` (sender)
   - `DataHandler.record_transaction()` (recipient)
   - Return to main menu

### View Transaction History Flow:

1. `BlockchainApp.run()` → `TransactionUI.view_transaction_history()`
   - `DataHandler.load_wallet_transactions()`
   - Display transactions
   - User input to return to main menu

### View Contact Transactions Flow:

1. `BlockchainApp.run()` → `TransactionUI.view_contact_transactions()`
   - `DataHandler.load_contacts()`
   - User selects contact
   - `DataHandler.load_wallet_transactions()`
   - Display transactions
   - User input to return to main menu

</div>

## ⛓️ Blockchain Flows

<div style="background-color: #fce4ec; padding: 15px; border-radius: 8px; border-left: 5px solid #e91e63;">

### Mine Transactions Flow:

1. `BlockchainApp.run()` → `BlockchainUI.mine_transactions()`
   - Check pending transactions
   - User confirms mining
   - `Blockchain.mine_pending_transactions()`
     - `Blockchain._validate_pending_transactions()`
     - `Blockchain._create_block()`
     - `DataHandler.save_blockchain()`
     - `DataHandler.save_pending_transactions()`
   - Return to main menu

### View Blockchain Flow:

1. `BlockchainApp.run()` → `BlockchainUI.view_blockchain()`
   - Display blockchain info
   - `Blockchain.validate_chain()`
   - User chooses to view details
   - If yes, display block details
   - Return to main menu

</div>

## 👛 Wallet Management Flows

<div style="background-color: #f3e5f5; padding: 15px; border-radius: 8px; border-left: 5px solid #9c27b0;">

### Select Wallet Flow:

1. `BlockchainApp.run()` → `WalletUI.select_wallet()`
   - `DataHandler.load_wallets()`
   - Display wallet options
   - User selects wallet or creates new one
   - Return selected wallet to main menu

### Create Wallet Flow:

1. `WalletUI.select_wallet()` → `WalletUI.create_wallet()`
   - User enters wallet details
   - `DataHandler.name_exists_in_contacts()` (validation)
   - Generate wallet address
   - `DataHandler.load_wallets()`
   - `DataHandler.save_wallets()`
   - Create corresponding contact
     - `DataHandler.load_contacts()`
     - `DataHandler.save_contacts()`
   - Return new wallet to caller

</div>

## 👥 Contact Management Flows

<div style="background-color: #f1f8e9; padding: 15px; border-radius: 8px; border-left: 5px solid #8bc34a;">

### Manage Contacts Flow:

1. `BlockchainApp.run()` → `ContactsUI.manage_contacts()`
   - Display contacts management menu
   - User selects option

2. Add Contact Option:
   - `ContactsUI.manage_contacts()` → `ContactsUI._add_contact()`
     - User enters contact details
     - `DataHandler.name_exists_in_contacts()` (validation)
     - Generate contact address
     - `DataHandler.load_contacts()`
     - `DataHandler.save_contacts()`
     - Return to contacts menu

3. Delete Contact Option:
   - `ContactsUI.manage_contacts()` → `ContactsUI._delete_contact()`
     - User selects contact to delete
     - `DataHandler.load_contacts()`
     - `DataHandler.save_contacts()`
     - Return to contacts menu

4. Edit Contact Option:
   - `ContactsUI.manage_contacts()` → `ContactsUI._edit_contact()`
     - User selects contact to edit
     - User enters new details
     - `DataHandler.name_exists_in_contacts()` (validation)
     - `DataHandler.load_contacts()`
     - `DataHandler.save_contacts()`
     - Return to contacts menu

5. Return to Main Menu Option:
   - `ContactsUI.manage_contacts()` → back to `BlockchainApp.run()`

</div>

## 📊 Function Call Diagrams

<div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 5px solid #9e9e9e;">

For visual representation of function calls, please refer to the following diagrams:

- [Application Startup Diagram](FUNCTION_FLOWS/startup_flow.md)
- [Transaction Flow Diagram](FUNCTION_FLOWS/transaction_flow.md)
- [Blockchain Flow Diagram](FUNCTION_FLOWS/blockchain_flow.md)
- [Wallet Management Diagram](FUNCTION_FLOWS/wallet_flow.md)
- [Contact Management Diagram](FUNCTION_FLOWS/contact_flow.md)

</div>

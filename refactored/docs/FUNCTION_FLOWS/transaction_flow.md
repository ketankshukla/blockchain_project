# 💸 Transaction Function Flow Diagram

<div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 5px solid #2196f3;">

This document visualizes the function call sequence during transaction-related operations.

</div>

## Send Transaction Flow

```mermaid
graph TD
    A[BlockchainApp.run] -->|Option 1| B[TransactionUI.send_transaction]
    B -->|Check balance| C{Sufficient Balance?}
    C -->|No| D[Return to Main Menu]
    C -->|Yes| E[DataHandler.load_contacts]
    E --> F{Contacts Available?}
    F -->|No| D
    F -->|Yes| G[Display Contacts]
    G --> H{User Selects Recipient}
    H -->|Cancel| D
    H -->|Select| I[User Enters Amount]
    I --> J{User Confirms?}
    J -->|No| D
    J -->|Yes| K[Blockchain.create_transaction]
    K --> L1[DataHandler.update_wallet_balance - Sender]
    L1 --> L2[DataHandler.update_wallet_balance - Recipient]
    L2 --> M1[DataHandler.record_transaction - Sender]
    M1 --> M2[DataHandler.record_transaction - Recipient]
    M2 --> N[Return to Main Menu]
```

## View Transaction History Flow

```mermaid
graph TD
    A[BlockchainApp.run] -->|Option 4| B[TransactionUI.view_transaction_history]
    B --> C[DataHandler.load_wallet_transactions]
    C --> D{Transactions Found?}
    D -->|No| E[Display No Transactions Message]
    D -->|Yes| F[Display Transactions]
    E --> G[User Input to Return]
    F --> G
    G --> H[Return to Main Menu]
```

## View Contact Transactions Flow

```mermaid
graph TD
    A[BlockchainApp.run] -->|Option 5| B[TransactionUI.view_contact_transactions]
    B --> C[DataHandler.load_contacts]
    C --> D{Contacts Available?}
    D -->|No| E[Display No Contacts Message]
    D -->|Yes| F[Display Contacts]
    F --> G{User Selects Contact}
    G -->|Cancel| H[Return to Main Menu]
    G -->|Select| I[DataHandler.load_wallet_transactions]
    I --> J{Transactions Found?}
    J -->|No| K[Display No Transactions Message]
    J -->|Yes| L[Display Transactions]
    K --> M[User Input to Return]
    L --> M
    M --> H
```

## Function Call Sequence: Send Transaction

### Initialization Phase

1. `BlockchainApp.run()` → `TransactionUI.send_transaction(current_wallet)`
   - Receives the current wallet as an argument
   - Extracts sender address and balance

### Validation Phase

2. Check sender balance
   - If insufficient, display message and return to main menu
   
3. `DataHandler.load_contacts()`
   - Load potential recipients
   - Filter out the current wallet from contacts
   - If no contacts available, display message and return to main menu

### Selection Phase

4. Display recipient selection menu
   - List all available contacts
   - Provide option to cancel

5. Process user selection
   - If canceled, return to main menu
   - If valid selection, proceed to amount entry

### Transaction Creation Phase

6. Get transaction amount from user
   - Validate using `validate_positive_number()`
   - Ensure amount does not exceed balance

7. Confirm transaction
   - Display transaction details
   - Get confirmation from user
   - If not confirmed, return to main menu

### Transaction Processing Phase

8. `Blockchain.create_transaction()`
   - Create transaction with sender, recipient, and amount
   
9. Update wallet balances
   - `DataHandler.update_wallet_balance()` for sender (subtract amount)
   - `DataHandler.update_wallet_balance()` for recipient (add amount)
   
10. Record transaction
    - `DataHandler.record_transaction()` for sender
    - `DataHandler.record_transaction()` for recipient
    
11. Return to main menu

## Function Call Sequence: View Transaction History

1. `BlockchainApp.run()` → `TransactionUI.view_transaction_history(address)`
   - Receives wallet address as an argument
   
2. `DataHandler.load_wallet_transactions(address)`
   - Load all transactions for the specified wallet
   
3. Display transactions
   - Format and display using tabulate
   - If no transactions, display appropriate message
   
4. Wait for user input and return to main menu

## Function Call Sequence: View Contact Transactions

1. `BlockchainApp.run()` → `TransactionUI.view_contact_transactions()`
   
2. `DataHandler.load_contacts()`
   - Load all contacts
   - If no contacts, display message and return to main menu
   
3. Display contact selection menu
   - List all contacts
   - Provide option to cancel
   
4. Process user selection
   - If canceled, return to main menu
   - If valid selection, proceed to transaction loading
   
5. `DataHandler.load_wallet_transactions(address)`
   - Load all transactions for the selected contact
   
6. Display transactions
   - Format and display using tabulate
   - If no transactions, display appropriate message
   
7. Wait for user input and return to main menu

## Return to Main Documentation

[Return to Function Flows Documentation](../FUNCTION_FLOWS.md)

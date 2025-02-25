# 🚀 Application Startup Function Flow Diagram

<div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 5px solid #4caf50;">

This document visualizes the function call sequence during application startup.

</div>

## Startup Sequence

```mermaid
graph TD
    A[main.py: __main__] --> B[BlockchainApp.__init__]
    B --> C1[DataHandler.__init__]
    B --> C2[Blockchain.__init__]
    B --> C3[WalletUI.__init__]
    B --> C4[TransactionUI.__init__]
    B --> C5[BlockchainUI.__init__]
    B --> C6[ContactsUI.__init__]
    A --> D[BlockchainApp.run]
    
    D --> E{Initial Menu}
    E -->|Option 1: Continue| F[WalletUI.select_wallet]
    E -->|Option 2: Exit| G[sys.exit]
    
    F --> H{Wallet Selected?}
    H -->|Yes| I[Display Main Menu]
    H -->|No| E
    
    I --> J{Main Menu Choice}
    J -->|Option 1| K1[TransactionUI.send_transaction]
    J -->|Option 2| K2[BlockchainUI.mine_transactions]
    J -->|Option 3| K3[BlockchainUI.view_blockchain]
    J -->|Option 4| K4[TransactionUI.view_transaction_history]
    J -->|Option 5| K5[TransactionUI.view_contact_transactions]
    J -->|Option 6| K6[ContactsUI.manage_contacts]
    J -->|Option 7| K7[WalletUI.select_wallet]
    J -->|Option 8| K8[sys.exit]
    
    K1 --> I
    K2 --> I
    K3 --> I
    K4 --> I
    K5 --> I
    K6 --> I
    K7 --> H
```

## Function Call Sequence

### Initialization Phase

1. `main.py` → `__main__` block
   - Creates the BlockchainApp instance
   - Calls `app.run()`

2. `BlockchainApp.__init__()`
   - Sets up directory paths
   - Initializes DataHandler with the parent directory path
   - Initializes Blockchain with the DataHandler
   - Initializes UI components:
     - WalletUI
     - TransactionUI
     - BlockchainUI
     - ContactsUI
   - Sets current_wallet to None

### Initial Menu Phase

3. `BlockchainApp.run()`
   - Displays the initial menu with two options:
     - Option 1: Continue to application
     - Option 2: Exit
   - If Option 2 is selected:
     - Displays exit message
     - Calls `sys.exit(0)`
   - If Option 1 is selected:
     - Continues to wallet selection

### Wallet Selection Phase

4. `WalletUI.select_wallet()`
   - Calls `DataHandler.load_wallets()`
   - Displays existing wallets
   - Provides options:
     - Select an existing wallet
     - Create a new wallet (calls `WalletUI.create_wallet()`)
     - Cancel operation
   - Returns selected wallet or None
   
5. Back to `BlockchainApp.run()`
   - If no wallet selected, prompts user and returns to initial menu
   - If wallet selected, displays user info and proceeds to main menu

### Main Menu Phase

6. Main Menu in `BlockchainApp.run()`
   - Displays the main menu with options
   - Gets user choice
   - Routes to appropriate UI method based on choice
   - After UI method completes, returns to main menu loop

## Data Flow

During the startup sequence, the following data is passed between functions:

```mermaid
graph TD
    A[BlockchainApp.__init__] -->|data_dir| B[DataHandler.__init__]
    B -->|data_handler| C[Blockchain.__init__]
    B -->|data_handler| D[WalletUI.__init__]
    B -->|data_handler| E[TransactionUI.__init__]
    C -->|blockchain| E
    B -->|data_handler| F[BlockchainUI.__init__]
    C -->|blockchain| F
    B -->|data_handler| G[ContactsUI.__init__]
    D -->|wallet| H[BlockchainApp.run]
```

## Return to Main Documentation

[Return to Function Flows Documentation](../FUNCTION_FLOWS.md)

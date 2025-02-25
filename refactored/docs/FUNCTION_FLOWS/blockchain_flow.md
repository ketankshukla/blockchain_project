# ⛓️ Blockchain Function Flow Diagram

<div style="background-color: #fce4ec; padding: 15px; border-radius: 8px; border-left: 5px solid #e91e63;">

This document visualizes the function call sequence during blockchain-related operations.

</div>

## Mine Transactions Flow

```mermaid
graph TD
    A[BlockchainApp.run] -->|Option 2| B[BlockchainUI.mine_transactions]
    B --> C{Pending Transactions?}
    C -->|No| D[Return to Main Menu]
    C -->|Yes| E[Display Transaction Count]
    E --> F{User Confirms Mining?}
    F -->|No| D
    F -->|Yes| G[Blockchain.mine_pending_transactions]
    
    G --> H[Blockchain._validate_pending_transactions]
    H --> I[Blockchain._create_block]
    I --> J[Block.calculate_hash]
    J --> K[Blockchain._proof_of_work]
    K --> L[DataHandler.save_blockchain]
    L --> M[DataHandler.save_pending_transactions]
    M --> N[DataHandler.update_wallet_balance]
    N --> O[DataHandler.record_transaction]
    O --> P[Display Success Message]
    P --> Q[Return to Main Menu]
```

## View Blockchain Flow

```mermaid
graph TD
    A[BlockchainApp.run] -->|Option 3| B[BlockchainUI.view_blockchain]
    B --> C[Display Chain Length]
    C --> D[Display Pending Transactions Count]
    D --> E[Blockchain.validate_chain]
    E --> F[Display Chain Validity]
    F --> G{View Block Details?}
    G -->|No| H[Return to Main Menu]
    G -->|Yes| I[Display Block Details]
    I --> J[Format Block Information]
    J --> K{Continue to Next Block?}
    K -->|Yes| I
    K -->|No| H
```

## Function Call Sequence: Mine Transactions

### Initialization Phase

1. `BlockchainApp.run()` → `BlockchainUI.mine_transactions(current_wallet)`
   - Receives the current wallet as an argument
   - This wallet will receive the mining reward

### Validation Phase

2. Check pending transactions
   - Get count from `blockchain.pending_transactions`
   - If no pending transactions, display message and return to main menu

### Confirmation Phase

3. Display pending transaction count
   - Show how many transactions will be processed
   
4. Get user confirmation
   - If not confirmed, return to main menu

### Mining Phase

5. `Blockchain.mine_pending_transactions(miner_address)`
   - Validates pending transactions with `_validate_pending_transactions()`
   - Creates a new block with `_create_block()`
   - Calculates block hash with `Block.calculate_hash()`
   - Performs proof of work with `_proof_of_work()`
   - Adds the new block to the chain
   - Creates a reward transaction for the miner
   
6. Save blockchain state
   - `DataHandler.save_blockchain()`
   - `DataHandler.save_pending_transactions()` (which is now empty)
   
7. Process mining reward
   - `DataHandler.update_wallet_balance()` to add reward to miner's wallet
   - `DataHandler.record_transaction()` to record the reward transaction
   
8. Display success message and return to main menu

## Function Call Sequence: View Blockchain

### Display Blockchain Info Phase

1. `BlockchainApp.run()` → `BlockchainUI.view_blockchain()`
   
2. Display basic blockchain information
   - Chain length (number of blocks)
   - Pending transaction count
   
3. `Blockchain.validate_chain()`
   - Validates the integrity of the entire blockchain
   - Returns boolean indicating validity
   
4. Display chain validity

### Block Details Phase

5. Get user input on whether to view block details
   - If no, return to main menu
   
6. If yes, for each block in the chain:
   - Display block header information (index, timestamp, hashes, nonce)
   - If not genesis block, display transactions in the block
   - Format addresses using contact names where available
   
7. After displaying all blocks, return to main menu

## Blockchain Data Structure

The blockchain consists of a chain of blocks with the following structure:

```mermaid
classDiagram
    class Blockchain {
        +chain: List[Block]
        +pending_transactions: List[Dict]
        +mining_reward: float
        +difficulty: int
        +__init__(data_handler)
        +create_transaction(sender, recipient, amount)
        +mine_pending_transactions(miner_address)
        +validate_chain()
        -_create_block(previous_hash)
        -_get_last_block()
        -_proof_of_work(block)
        -_validate_pending_transactions()
    }
    
    class Block {
        +index: int
        +timestamp: float
        +transactions: List[Dict]
        +previous_hash: str
        +nonce: int
        +hash: str
        +__init__(index, timestamp, transactions, previous_hash)
        +calculate_hash()
    }
    
    Blockchain "1" o-- "many" Block
```

## Return to Main Documentation

[Return to Function Flows Documentation](../FUNCTION_FLOWS.md)

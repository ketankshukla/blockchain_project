# 📱 User Guide

<div style="background-color: #e6f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #1890ff;">

Welcome to the **Simple Blockchain Application**! This guide will help you understand how to use the application and make the most of its features.

</div>

## 💡 Introduction

<div style="background-color: #fffbe6; padding: 15px; border-radius: 8px; border-left: 5px solid #faad14;">

This application allows you to:

- Create digital wallets
- Send and receive digital coins
- Mine new blocks to earn rewards
- Track transaction history
- Manage contacts

The application uses blockchain technology to ensure secure and transparent transactions.

</div>

## 🚀 Getting Started

<div style="background-color: #f6ffed; padding: 15px; border-radius: 8px; border-left: 5px solid #52c41a;">

### Starting the Application

1. Open a command prompt or terminal
2. Navigate to the application directory
3. Run the application:
   ```bash
   python main.py
   ```
4. You'll be presented with the main menu

### Creating Your First Wallet

1. From the main menu, select "Switch Wallet" (option 7)
2. Select "N" to create a new wallet
3. Enter your first and last name
4. Your wallet will be created with a starting balance of 100 coins

</div>

## 📡 Main Features

<div style="background-color: #f9f0ff; padding: 15px; border-radius: 8px; border-left: 5px solid #722ed1;">

### 💸 Sending Transactions

1. From the main menu, select "Send Transaction" (option 1)
2. Choose a recipient from your contacts
3. Enter the amount to send
4. Confirm the transaction details
5. The transaction will be added to the pending transactions list

**Example:**
```
=== Send Transaction ===
Your balance: 100

Select Recipient:
1. Bob Banderas
2. Sally Smothers

Enter recipient number or X to cancel: 1
Enter amount to send to Bob (max 100): 10

Transaction Details:
From: Your Wallet
To: Bob Banderas
Amount: 10

Confirm transaction? (y/n): y

Transaction completed successfully!
```

### ⛏️ Mining Transactions

1. From the main menu, select "Mine Transactions" (option 2)
2. Confirm that you want to start mining
3. The application will perform proof-of-work calculations
4. When complete, you'll receive a mining reward of 10 coins

**Example:**
```
Mining pending transactions...
Pending transactions: 3

Start mining? (press Enter to cancel): y

Block mined successfully! 3 transactions processed.
Mining reward: 10 coins added to your wallet
```

### 📊 Viewing Blockchain

1. From the main menu, select "View Blockchain" (option 3)
2. You'll see general information about the blockchain
3. You can choose to view detailed block information

**Example:**
```
=== Blockchain Info ===
 Chain length: 3 blocks
 Pending transactions: 2
 Chain validity: Valid

View block details? (press Enter to skip): y

 Block #0
==================================================
┌──────────┬────────────┐
│ Index    │     0      │
│ Timestamp│  2025-02-25 10:15:22  │
│ Previous Hash│ 0                                                             │
│ Hash     │ 018d430572d0c41e9dfe6199138808c9ff77f0a68b5d3db492516a3129a3fcd1 │
│ Nonce    │     0      │
└──────────┴────────────┘

Genesis Block
```

### 📜 Viewing Transaction History

1. From the main menu, select "View My Transactions" (option 4)
2. You'll see a list of all transactions involving your wallet

**Example:**
```
 Transaction History for Ketan Shukla
==================================================

┌──────────────┬──────────────┬──────────────────────────────────────────────┬──────────────────────────────────────────────┬─────────────────┐
│     Type     │    Amount    │                     From                      │                      To                       │       Time      │
├──────────────┼──────────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼─────────────────┤
│     SENT     │     3.00     │       Ketan Shukla (d8fa19...)                │        Eddie Garvin (5fe227...)              │ 2025-02-25 10:05:59 │
│    REWARD    │    10.00     │           🏆 Mining Reward                    │       Ketan Shukla (d8fa19...)                │ 2025-02-25 10:06:44 │
└──────────────┴──────────────┴──────────────────────────────────────────────┴──────────────────────────────────────────────┴─────────────────┘
```

### 👥 Managing Contacts

1. From the main menu, select "Manage Contacts" (option 6)
2. You can:
   - Add new contacts
   - Delete existing contacts
   - Edit contact information

**Example:**
```
=== Manage Contacts ===
Found 4 contact(s)

Existing Contacts:
1. Ketan Shukla
2. Bob Banderas
3. Sally Smothers
4. Eddie Garvin

Options:
1. Add New Contact
2. Delete Contact
3. Edit Contact
4. Return to Main Menu

Enter option (1-4): 1

=== Add New Contact ===
Enter First Name: Jane
Enter Last Name: Smith

Contact added: Jane Smith
Address: a1b2c3d4e5f6...
```

</div>

## ❓ Frequently Asked Questions

<div style="background-color: #fff2e8; padding: 15px; border-radius: 8px; border-left: 5px solid #fa541c;">

### What is blockchain?
A blockchain is a distributed ledger that records transactions across multiple computers. Each block contains a list of transactions and is linked to the previous block, forming a chain.

### How do I earn coins?
You can earn coins by mining blocks. Each time you mine a block, you receive a mining reward of 10 coins.

### Are my transactions private?
Transactions are recorded on the blockchain and can be viewed by anyone using the application. However, only wallet addresses are shown, not your personal information.

### What happens if I lose my wallet?
Currently, wallets are stored in a local file. If you delete this file, you will lose access to your wallet and its funds.

### Can I have multiple wallets?
Yes, you can create multiple wallets and switch between them.

</div>

## ❌ Troubleshooting

<div style="background-color: #fff1f0; padding: 15px; border-radius: 8px; border-left: 5px solid #f5222d;">

### Common Issues

#### "Insufficient balance" when sending transactions
- Check your wallet balance
- Make sure you're not trying to send more coins than you have

#### No pending transactions to mine
- Transactions need to be created before they can be mined
- Send a transaction first, then try mining

#### Contact with the same name already exists
- Each contact must have a unique name
- Use a different name or edit the existing contact

#### Transaction not appearing in history
- Transactions must be mined into a block before appearing in the completed transaction history
- Check if the transaction is still pending

</div>

## ❓ Troubleshooting

<div style="background-color: #fff0f6; padding: 15px; border-radius: 8px; border-left: 5px solid #eb2f96;">

### Common Issues

#### The Application Doesn't Start

- Ensure you are in the correct directory (`refactored`)
- Make sure Python is installed and in your PATH
- Check that you have activated the virtual environment if using one

#### Transaction Errors

- Check that you have sufficient balance for the transaction
- Verify that the recipient exists in your contacts
- Ensure that the network connection is stable

#### Mining Issues

- Mining takes computational power and may take longer on slower systems
- Ensure there are pending transactions to mine
- Check that your blockchain data files are not corrupted

### Need More Help?

If you encounter persistent issues, please contact the developer or create an issue in the project repository.

</div>

## 🔧 Advanced Features

<div style="background-color: #fcffe6; padding: 15px; border-radius: 8px; border-left: 5px solid #a0d911;">

### Blockchain Validation
The application automatically validates the blockchain integrity by checking:
- Each block's hash is correctly calculated
- Each block references the previous block's hash
- No blocks have been tampered with

### Proof of Work
The mining process uses a proof-of-work algorithm:
- The system must find a value (nonce) that results in a hash starting with a specific number of zeros
- The difficulty can be adjusted to make mining easier or harder

</div>

## 📝 Sample Workflows

<div style="background-color: #e6fffb; padding: 15px; border-radius: 8px; border-left: 5px solid #13c2c2;">

### Complete Transaction Flow

1. Create a wallet for yourself
2. Create a wallet or contact for the recipient
3. Send a transaction from your wallet to the recipient
4. Mine the transaction to include it in the blockchain
5. View the transaction in your transaction history

### Setting Up Multiple Users

1. Create multiple wallets
2. Switch between wallets using the "Switch Wallet" option
3. Send transactions between these wallets
4. Each wallet maintains its own transaction history

</div>

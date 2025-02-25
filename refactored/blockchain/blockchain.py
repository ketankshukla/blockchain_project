import time
from typing import List, Dict, Any, Optional
from blockchain.block import Block
from blockchain.transaction import Transaction


class Blockchain:
    """
    Represents a blockchain, which is a chain of blocks containing transaction records.
    Implements methods for adding blocks, validating the chain, and managing transactions.
    """
    def __init__(self, data_handler, difficulty: int = 4, mining_reward: int = 10):
        """
        Initialize a new blockchain.
        
        Args:
            data_handler: Handler for loading and saving blockchain data
            difficulty: Difficulty level for proof-of-work (more zeros required)
            mining_reward: Reward amount for mining a block
        """
        self.data_handler = data_handler
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.chain = self.load_blockchain()
        if not self.chain:
            self.chain = [self.create_genesis_block()]
            self.save_blockchain()
        self.pending_transactions = []
        self.load_pending_transactions()

    def load_blockchain(self) -> List[Block]:
        """
        Load blockchain data from storage.
        If no blockchain file exists, attempt to reconstruct from completed transactions.
        
        Returns:
            List of Block objects representing the blockchain
        """
        chain_data = self.data_handler.load_blockchain()
        if chain_data:
            print("Loading existing blockchain...")
            # Convert dictionary objects back to Block objects
            chain = [Block(
                block['index'],
                block['timestamp'],
                block['transactions'],
                block['previous_hash'],
                block['nonce']
            ) for block in chain_data]
            
            # Recalculate all block hashes to ensure chain integrity
            for i in range(len(chain)):
                if i == 0:  # Genesis block
                    chain[i].hash = chain[i].calculate_hash()
                else:
                    # Ensure previous_hash is correct
                    chain[i].previous_hash = chain[i-1].hash
                    # Recalculate current block's hash
                    chain[i].hash = chain[i].calculate_hash()
            
            # Save the chain with updated hashes
            self.chain = chain
            self.save_blockchain()
            return chain
        
        print("No blockchain file found, reconstructing from completed transactions...")
        # If no blockchain file exists, reconstruct from completed transactions
        completed_transactions = self.data_handler.load_completed_transactions()
        if not completed_transactions:
            print("No completed transactions found.")
            return []
            
        print(f"Found {len(completed_transactions)} completed transactions")
        
        # Group transactions by mining rewards
        chain = [self.create_genesis_block()]
        current_block_txs = []
        
        for tx in completed_transactions:
            current_block_txs.append(tx)
            # When we find a reward transaction, that marks the end of a block
            if tx.get('type') == 'REWARD':
                # Create a new block with these transactions
                new_block = Block(
                    len(chain),
                    tx['timestamp'],  # Use reward transaction timestamp
                    current_block_txs,
                    chain[-1].hash
                )
                new_block.hash = new_block.calculate_hash()
                chain.append(new_block)
                current_block_txs = []  # Start a new block
        
        # If any transactions left without a reward, add them as a final block
        if current_block_txs:
            new_block = Block(
                len(chain),
                current_block_txs[-1]['timestamp'],
                current_block_txs,
                chain[-1].hash
            )
            new_block.hash = new_block.calculate_hash()
            chain.append(new_block)
        
        print(f"Created blockchain with {len(chain)} blocks")
        
        # Save the reconstructed chain
        self.chain = chain
        self.save_blockchain()
        return chain

    def save_blockchain(self) -> None:
        """Save the current blockchain state to storage."""
        try:
            # Convert Block objects to dictionaries for JSON serialization
            chain_data = [{
                'index': block.index,
                'timestamp': block.timestamp,
                'transactions': block.transactions,
                'previous_hash': block.previous_hash,
                'nonce': block.nonce,
                'hash': block.hash
            } for block in self.chain]
            self.data_handler.save_blockchain(chain_data)
            print(f"Saved blockchain with {len(chain_data)} blocks")
        except Exception as e:
            print(f"Error saving blockchain: {str(e)}")

    def load_pending_transactions(self) -> None:
        """Load pending transactions from storage."""
        self.pending_transactions = self.data_handler.load_pending_transactions()

    def save_pending_transactions(self) -> None:
        """Save pending transactions to storage."""
        self.data_handler.save_pending_transactions(self.pending_transactions)

    def create_genesis_block(self) -> Block:
        """
        Create the first block in the chain (genesis block).
        
        Returns:
            A Block object representing the genesis block
        """
        return Block(0, time.time(), "Genesis Block", "0")

    def get_last_block(self) -> Block:
        """
        Get the most recent block in the chain.
        
        Returns:
            The last Block object in the chain
        """
        return self.chain[-1]

    def create_transaction(self, sender: str, receiver: str, amount: float) -> Dict[str, Any]:
        """
        Create a new transaction and add it to pending transactions.
        
        Args:
            sender: Address of the sender
            receiver: Address of the receiver
            amount: Amount of coins transferred
            
        Returns:
            Dictionary representation of the created transaction
        """
        transaction = Transaction(sender, receiver, amount)
        tx_dict = transaction.to_dict()
        self.pending_transactions.append(tx_dict)
        self.save_pending_transactions()
        return tx_dict

    def mine_pending_transactions(self, miner_address: str) -> int:
        """
        Mine pending transactions and create a new block.
        
        Args:
            miner_address: Address of the miner who will receive the reward
            
        Returns:
            Number of transactions processed
            
        Raises:
            ValueError: If there are no pending transactions
        """
        # Load pending transactions
        pending_transactions = self.data_handler.load_pending_transactions()
        if not pending_transactions:
            return 0  # Return number of transactions processed

        # Create mining reward transaction
        reward_transaction = {
            'sender': "Network Reward",
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
        self.save_blockchain()  # Save the updated chain

        # Update completed transactions
        completed_transactions = self.data_handler.load_completed_transactions()
        completed_transactions.extend(pending_transactions + [reward_transaction])
        self.data_handler.save_completed_transactions(completed_transactions)

        # Clear pending transactions
        self.data_handler.save_pending_transactions([])
        self.pending_transactions = []

        # Update miner's wallet with reward
        self.data_handler.update_wallet_balance(miner_address, self.mining_reward)
        
        # Record reward transaction
        self.data_handler.record_transaction(reward_transaction, miner_address, "Network Reward")

        return len(pending_transactions)  # Return number of transactions processed

    def proof_of_work(self, block: Block) -> int:
        """
        Implement proof-of-work algorithm by finding a nonce that produces a hash
        with a specific number of leading zeros determined by difficulty.
        
        Args:
            block: The block to mine
            
        Returns:
            The nonce value that satisfies the difficulty requirement
        """
        block.nonce = 0
        computed_hash = block.calculate_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.calculate_hash()
        return block.nonce

    def validate_chain(self) -> bool:
        """
        Validate the integrity of the blockchain by checking each block's hash
        and references to previous blocks.
        
        Returns:
            True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True

import hashlib
import json
import random
import time
from datetime import datetime


class Validator:

    def __init__(self):
        self.stakes = {}

    # Adds the specified stake to the given node in the stakes dictionary.
    #   If the node already exists in the dictionary, the stake is updated.
    #   If the node does not exist, a new entry is created with the specified stake.
    def add_stake(self, node, stake):
        self.stakes[node] = stake

    # return {str(node): self.stakes[node] for node in self.stakes}
    # Returns a dictionary containing all the stakes for each node in the validator.
    #     The keys are the nodes and the values are their respective stakes.
    def show_all_stakes(self):
        return self.stakes

    # Increases the stake of the specified node by the given amount.
    #   If the node is not in the stakes' dictionary, a new entry is created with the specified amount.
    def increase_stake(self, node, amount):
        if node in self.stakes:
            self.stakes[node] += amount

    #  Decreases the stake of the specified node by the given amount.
    #  If the node is found in the stakes' dictionary, the stake is decreased by the amount.
    def decrease_stake(self, node, amount):
        if node in self.stakes:
            self.stakes[node] -= amount

    #    Returns the stake of the specified node from the stakes' dictionary.
    #    If the node is not found, returns None.
    def show_stake(self, node):
        if node in self.stakes:
            return self.stakes[node]
        else:
            return None


class Blockchain:
    penalty_amount = 100
    miner_fees = 100
    validator_fees = 50
    validator = Validator()

    def __init__(self):
        self.transactions = []
        self.chain = []
        self.atomic_transactions = {}
        self.verified_atomic_transactions = {}
        self.incomplete_verified_atomic_transactions = {}
        # self.nodes = set()
        self.chain.append(self.create_block("GENESIS", -1))

    # Creates a new block with the given miner, previous hash, and optional fault.
    #   If the miner is "GENESIS", a special block for the genesis block is created.
    #   Otherwise, a block is created with the specified miner, previous hash,
    #    and an optional fault if provided.
    def create_block(self, miner, previous_hash=None, fault=None):
        if miner == "GENESIS":
            block = {
                'index': len(self.chain) + 1,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'miner': miner,
                'previous_hash': previous_hash,
            }
            return block
        else:
            transactions = self.stringify(self.transactions)
            if fault == 1:
                transactions.append("I am a forged transaction")
            block = {
                'index': len(self.chain) + 1,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'miner': miner,
                'previous_hash': previous_hash,
                # 'transactions': self.transactions,
                'transactions': transactions,
                'merkle_root': self.calculate_merkle_root(transactions)
            }

            return block

    #    Converts a list of transactions into a list of formatted strings for hashing
    @staticmethod
    def stringify(transactions):
        list_of_strings = []
        for transaction in transactions:
            transaction_string = (
                f"Type: {transaction['type']}, "
                f"Product: {transaction['product']}, "
                f"Manufacturer: {transaction['manufacturer']}, "
                f"Distributor: {transaction['distributor']}, "
                f"Client: {transaction['client']}, "
                f"Timestamp: {transaction['timestamp']}, "
                f"Distributor Received At: {transaction['distributor_received_at']}, "
                f"Distributor Dispatched At: {transaction['distributor_dispatched_at']}, "
                f"Client Received At: {transaction['client_received_at']}, "
            )
            list_of_strings.append(transaction_string)
        return list_of_strings

    #    Returns the previous block in the blockchain.
    #    The previous block is determined by the current block's previous hash.
    #   If no previous block is found (e.g., for the genesis block), returns None.
    def get_previous_block(self):
        if not self.chain:
            self.create_block("GENESIS", -1)
        return self.chain[-1]

    """
    Adds an atomic transaction to the blockchain.
    An atomic transaction is a transaction that must be executed as a whole,
    and if any part of it fails, the entire transaction is rolled back.
    """

    def add_atomic_transaction(self, sender, receiver, product, fault_type):

        if receiver.product and receiver.user_type == 'distributor':
            print("Error: Distributor can only have one product at a time!")
            return False

        if fault_type == 0:
            print('No fault response')

            if sender.user_type == 'manufacturer':
                sender.send_product_from_list(product)
            else:
                sender.send_product()

            time.sleep(1)
            receiver.receive_product(product)

        elif fault_type == 1:
            print("Fault 1 response")

            sender.send_product()
            time.sleep(1)
            receiver.receive_product(product, 1)

        elif fault_type == 2:
            print("Fault 2 response")

        if product not in self.atomic_transactions:
            self.atomic_transactions[product] = []

        transaction = {
            'sender': sender,
            'receiver': receiver,
            'product': product
        }

        self.atomic_transactions[product].append(transaction)

        return True

    """
    Adds a list of transactions to the blockchain.
    Each transaction in the list is appended to the blockchain's transaction pool.
    """

    def add_transactions(self):
        print("Adding transactions")
        for product, transactions in self.verified_atomic_transactions.items():
            transaction_info = {
                'type': 'COMPLETE',
                'product': product.product_name,
                'manufacturer': transactions[0]['sender'].user_name,
                'distributor': transactions[0]['receiver'].user_name,
                'client': transactions[1]['receiver'].user_name,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'distributor_received_at': product.history[1]['time'],
                'distributor_dispatched_at': None if len(product.history) <= 2 else product.history[2]['time'],
                'client_received_at': None if len(product.history) <= 3 else product.history[3]['time']
            }

            self.transactions.append(transaction_info)
        for product, transactions in self.incomplete_verified_atomic_transactions.items():
            transaction_info = {
                'type': 'INCOMPLETE',
                'product': product.product_name,
                'manufacturer': transactions[0]['sender'].user_name,
                'distributor': transactions[0]['receiver'].user_name,
                'client': None,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'distributor_received_at': None if len(product.history) <= 1 else product.history[1]['time'],
                'distributor_dispatched_at': None if len(product.history) <= 2 else product.history[2]['time'],
                'client_received_at': None if len(product.history) <= 3 else product.history[3]['time']
            }
            self.transactions.append(transaction_info)

    """
    Computes the hash value of the given block using a hashing algorithm.
    The block is first encoded as a JSON string and then hashed using the SHA256 algorithm.
    The resulting hash value is returned as a hexadecimal string.
    """

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    """
    Checks the validity of the given blockchain by verifying the integrity and consistency of its blocks.
    The function iterates through each block in the chain and checks if the previous hash matches the hash of the previous block.
    Returns True if the chain is valid, False otherwise.
    """

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            else:
                if not self.is_block_valid(current_block):
                    return False

        return True

    """
    Checks the validity of the given block by verifying its Merkle root.
    Returns True if the block is valid, False otherwise.
    """

    def is_block_valid(self, block, original_transactions):
        calculated_merkle_tree = self.calculate_merkle_root(original_transactions)
        present_merkle_tree = block['merkle_root']

        if calculated_merkle_tree != present_merkle_tree:
            return False

        return True

    """
    Implements the consensus algorithm to achieve agreement on the valid blockchain.
    Chooses the miner/forger and after he forges, the selected validators agree on the block's validate,
    and add the block to the blockchain 
    Returns True if the local chain is replaced, False otherwise.
    """

    def consensus(self, fault=None):
        """
        PoS Consensus Algorithm:
        Randomly select a leader to propose a new block, where higher stake equals higher chance.
        Other selected stakeholders validate and agree on the block.
        """

        leader = self.select_leader()  # Comes from the leader selection process
        original_transaction_string = self.stringify(self.transactions)
        proposed_block = self.create_block(miner=leader.user_name, previous_hash=self.hash(self.get_previous_block()),
                                           fault=fault)
        print(self.hash(self.chain[0]))
        print(leader.user_name)
        print(self.hash(proposed_block))
        # Validation by other stakeholders
        # After block gets validated:
        validators = [v for v in self.validator.stakes.keys() if v != leader]
        selected_validators = random.sample(validators, 2)

        # is_block_valid = all(self.is_block_valid(proposed_block) for validator in selected_validators)
        is_block_valid = self.is_block_valid(proposed_block, original_transaction_string)
        if is_block_valid:
            proposed_block['previous_hash'] = self.hash(self.get_previous_block())
            self.chain.append(proposed_block)
            self.transactions = []
            self.validator.add_stake(leader, self.miner_fees)
            for v in selected_validators:
                self.validator.add_stake(v, self.validator_fees)
            return self.hash(proposed_block)
        else:
            print("Block validation failed, penalty applied to the miner")
            self.validator.decrease_stake(leader, self.penalty_amount)

    """
    Uses simple recursion for generating merkle root needed for encrypting transactions
    """

    def calculate_merkle_root(self, transactions):
        if len(transactions) == 0:
            return None
        if len(transactions) == 1:
            return self.hash(transactions[0])

        # Recursive construction of the Merkle tree
        mid = len(transactions) // 2
        left_tree = self.calculate_merkle_root(transactions[:mid])
        right_tree = self.calculate_merkle_root(transactions[mid:])
        return self.hash(left_tree + right_tree)

    """
    Selects a random leader out of all the stakeholders, where the probability of the miner is directly proportional
    to the stake of the stakeholder. The randomness ensures that the highest stake holder isn't mining everytime
    """
    def select_leader(self):
        total_stake = sum(self.validator.stakes.values())
        random_stake = random.uniform(0, total_stake)
        current_stake = 0

        for node, stake in self.validator.stakes.items():
            current_stake += stake
            if current_stake >= random_stake:
                return node

    """
    verify the given atomic transactions to know if there is a fault in the Supply chain management
    """

    def verify_atomic_transaction(self):
        print("Placeholder")
        # print(self.atomic_transactions)
        products_to_remove = []
        for product, transactions in self.atomic_transactions.items():
            product_history = product.history
            print(f'for product {product.product_name} : {len(product_history)}')
            for pr in product_history:
                print(pr)
            for transaction in transactions:
                print(transaction)

            isVerifiedTransaction = 0
            isIncomplete = None
            if len(product_history) == 1 or len(transactions) == 1:
                isIncomplete = True
            elif len(product_history) == 2:
                print("Error: liar present")
                print(f"Liar: {transactions[-1]['sender']}")
                # transactions[-1]['sender'].penalty(self.penalty_amount)
                self.validator.decrease_stake(transactions[-1]['sender'], self.penalty_amount)
                isVerifiedTransaction = -2
            elif len(product_history) == 3:
                print("Error: liar present")
                t_id = 0
                # liar detection algo
                print(f"Liar: {transactions[-1]['receiver']}")
                # transactions[-1]['receiver'].penalty(self.penalty_amount)
                self.validator.decrease_stake(transactions[-1]['receiver'], self.penalty_amount)
                isVerifiedTransaction = -1
            elif len(product_history) == 4:
                index = 0
                for transaction in transactions:
                    sender, receiver = product_history[index], product_history[index + 1]
                    index += 2
                    print(f"Sender = {sender['at'].user_name}")
                    print(f"Receiver = {receiver['at'].user_name}")
                    if sender['at'] == transaction['sender']:
                        if sender['at'].productSend and not sender['at'].product:
                            print("Valid sender")
                    if receiver['at'] == transaction['receiver']:
                        if receiver['at'].user_type == 'distributor' and not receiver['at'].product:
                            print("Receiver was a distributor and the product was sent")
                        elif receiver['at'].productReceived and receiver['at'].product:
                            print("Valid receiver")
                        else:
                            print(f"Ghapla has been done by the receiver {receiver['at'].user_name}")

                isVerifiedTransaction = 1

            if isVerifiedTransaction != 0:
                self.verified_atomic_transactions[product] = transactions
                products_to_remove.append(product)
            if isIncomplete:
                self.incomplete_verified_atomic_transactions[product] = transactions
        for product in products_to_remove:
            self.atomic_transactions.pop(product)
        self.add_transactions()
        """
        Verifies the integrity and validity of an atomic transaction.
        The function checks if the transaction is properly signed and if the transaction data is consistent.
        Returns True if the transaction is valid, False otherwise.
        """


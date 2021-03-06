import json
from hashlib import sha256
from datetime import datetime
import time


class Transaction:

    def __init__(self, prev_address, address, amount=0, fee=0, time=time.time()):
        self.prev_address = prev_address
        self.address = address
        self.amount = amount
        self.fee = fee
        self.time = time


class Block:

    def __init__(self, prev_hash, transactions=[], difficulty=4, reward=10, timestamp=datetime.now()):
        self.difficulty = difficulty
        self.reward = reward
        self.proof = 0
        self.hash = None
        self.prev_hash = prev_hash
        self.timestamp = str(timestamp)
        self.transactions = transactions

    def create_hash(self):
        block_string = json.dumps({"proof": self.proof, "transactions": self.transactions})
        return sha256(block_string.encode()).hexdigest()

    def calculate(self):
        self.hash = self.create_hash()
        while not self.hash.startswith('0' * self.difficulty):
            self.proof += 1
            self.hash = self.create_hash()

    def mine_block(self, node_address, reward_address):
        reward_transaction = Transaction(prev_address=node_address, address=reward_address, amount=self.reward)
        self.transactions.append(reward_transaction.__dict__)
        self.calculate()


class Blockchain:

    def __init__(self, chain=[]):
        self.chain = chain
        if len(chain) == 0:
            self.create_genesis()

    def create_genesis(self):
        block = Block("0")
        block.calculate()
        self.chain.append(block)

    def is_chain_valid(self):
        for index, block in enumerate(self.chain, start=1):
            if self.chain[index-1].hash != block.hash:
                return False
            if not block.hash.startswith('0' * block.difficulty):
                return False
            if block.proof != block.create_hash():
                return False
        return True

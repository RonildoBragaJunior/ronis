from blockchain import Blockchain, Block
from uuid import uuid4
import requests
import json

headers = {'Content-Type': "application/json"}


class Node:
    def __init__(self, node_address=str(uuid4()), reward_address=str(uuid4()), unconfirmed_txn=[], mined_txn=[]):
        self.node_address = node_address
        self.reward_address = reward_address
        self.unconfirmed_txn = unconfirmed_txn
        self.mined_txn = mined_txn
        self.blockchain = Blockchain()
        self.network = []

    def add_nodes(self, nodes):
        for (k, v) in nodes.items():
            if v not in self.network:
                self.network.append(v)

    def add_unconfirmed_txn(self, transaction):
        self.unconfirmed_txn.append(transaction)

        # announce transaction on the network
        for node_address in self.network:
            requests.post(node_address + "/add_block",
                          data=json.dumps(transaction),
                          headers=headers)

    def mine_transactions(self):
        new_block = Block(
            prev_hash=self.blockchain.chain[-1].hash,
            transactions=self.unconfirmed_txn[0:5])
        new_block.mine_block(self.reward_address)
        self.blockchain.chain.append(new_block)

        # announce mined block on the network
        for peer_address in self.network:
            data = {"block": json.dumps(new_block.__dict__)}
            requests.post(peer_address + "/add_block", data=json.dumps(data), headers=headers)

    def compare_chains(self):
        for node_address in self.network:
            response = requests.get(node_address + "/chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                new_blockchain = Blockchain(chain)
                if length > len(self.blockchain.chain) and new_blockchain.is_chain_valid():
                    self.blockchain.chain = new_blockchain

        return self.blockchain.chain

import json
import requests
from node import Node
from blockchain import Transaction
from flask import request, jsonify, Flask

headers = {"Content-Type": "application/json"}
app = Flask(__name__)
node = Node()


@app.route("/register", methods=["GET"])
def register():
    data = {"address": request.url_root}
    response = requests.post("http://localhost:8000/add_node",
                             data=json.dumps(data),
                             headers=headers)
    return response.json()


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()
    transaction = Transaction(**data)
    node.add_unconfirmed_txn(transaction.__dict__)
    return "transaction received", 200


@app.route("/mine_transactions", methods=["GET"])
def mine_transactions():
    node.mine_transactions()
    return "New block mined", 200


@app.route("/get_blockchain", methods=["GET"])
def get_blockchain():
    response = jsonify([ob.__dict__ for ob in node.blockchain.chain])
    return response, 200


@app.route("/check_network_blockchain", methods=["GET"])
def check_network_blockchains():
    biggest_chain = node.compare_chains()
    result = {"chain": biggest_chain.chain, "length": len(biggest_chain.chain)}
    return result, 200


if __name__ == '__main__':
    app.run()

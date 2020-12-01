import requests
from flask import request, Flask, jsonify

from wallet import Transaction
from wallet import Wallet

headers = {"Content-Type": "application/json"}
app = Flask(__name__)
wallet = Wallet()


@app.route("/add_utxn", methods=["POST"])
def add_utxn():
    json = request.get_json()
    utxn = Transaction(
        prev_address=json["prev_address"],
        address=json["address"],
        amount=json["amount"]
    )
    wallet.utxns.append(utxn)

    return "ok", 200


@app.route("/get_utxns", methods=["GET"])
def get_utxns():
    result = jsonify([ob.__dict__ for ob in wallet.utxns])

    return result, 200


@app.route("/move_utxn", methods=["POST"])
def move_utxn():
    json = request.get_json()
    address, amount = json["address"], json["amount"]
    input_tx, total_input = [], 0

    for index in range(0, len(wallet.utxns)):
        input_tx.append(wallet.utxns[index])
        total_input += wallet.utxns[index].amount
        if total_input >= amount:
            new_transaction, rest_transaction = \
                wallet.move_transaction(input_tx, address, amount)
            break

    wallet.utxns.append(rest_transaction)

    response = requests.get("http://localhost:8000/get_nodes")
    if response.status_code == 200:
        nodes = response.json()["nodes"]
        for node in nodes:
            requests.post(node + "/add_transaction", data=json.dumps(new_transaction), headers=headers)

    return "ok", 200


if __name__ == '__main__':
    app.run()

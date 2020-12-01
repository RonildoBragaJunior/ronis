from flask import request, Flask
import requests
from wallet import Wallet
from random import seed, randint
import uuid
import time
import json

headers = {"Content-Type": "application/json"}
app = Flask(__name__)
wallet = Wallet()


@app.route("/move_transaction", methods=["GET"])
def move_transaction():
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

    return "unconfirmed transaction has been broadcast"


@app.route("/test", methods=["GET"])
def test():
    transactions = 1000

    def broadcast(self):
        headers = {'Content-Type': "application/json"}
        nodes = ["http://127.0.0.1:8000"]
        seed(1)

        for i in range(0, self.transactions):
            data = {"from": str(uuid.uuid4()), "to": str(uuid.uuid4()), "amt": randint(0, 1000), "time": time.time()}
            for node in nodes:
                requests.post(node + "/new_transaction", data=json.dumps(data), headers=headers)
                print(i)


if __name__ == '__main__':
    app.run()

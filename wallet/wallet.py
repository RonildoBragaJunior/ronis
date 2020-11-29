from flask import request, Flask
import requests

headers = {"Content-Type": "application/json"}
app = Flask(__name__)


@app.route("/transaction", methods=["GET"])
def transaction():
    unconfirmed_txn = request.get_json()

    response = requests.get("http://localhost:8000/get_nodes")
    if response.status_code == 200:
        nodes = response.json()["nodes"]
        for node in nodes:
            requests.post(node+"/add_transaction", data=unconfirmed_txn, headers=headers)

    return "unconfirmed transaction has been broadcast"


@app.route("/broadcast", methods=["GET"])
def broadcast():
    response = requests.get("http://localhost:8000/get_nodes")

    if response.status_code == 200:
        nodes = response.json()["nodes"]
        for node in nodes:
            print(node)


if __name__ == '__main__':
    app.run()

import uuid
import json
import time
import requests
from random import seed, randint


class Transactions:
    def __init__(self):
        self.transactions = 1000

    def broadcast(self):
        headers = {'Content-Type': "application/json"}
        nodes = ["http://127.0.0.1:8000"]
        seed(1)

        for i in range(0, self.transactions):
            data = {"from": str(uuid.uuid4()), "to": str(uuid.uuid4()), "amt": randint(0, 1000), "time": time.time()}
            for node in nodes:
                requests.post(node + "/new_transaction", data=json.dumps(data), headers=headers)
                print(i)


class Network:
    def __init__(self, nodes=[]):
        self.nodes = nodes
from flask import request, jsonify, Flask

app = Flask(__name__)
nodes = []


@app.route("/add_node", methods=["POST"])
def add_node():
    json = request.get_json()
    address = json["address"]
    nodes.append(address)
    return "node added to the network"


@app.route("/remove_node", methods=["POST"])
def remove_node():
    json = request.get_json()
    address = json["address"]
    nodes.remove(address)
    return "node removed to the network"


@app.route("/get_nodes", methods=["GET"])
def get_nodes():
    return jsonify(nodes)


if __name__ == '__main__':
    app.run()
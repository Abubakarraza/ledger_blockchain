from flask import Flask, jsonify, request
from blockchain import BlockChain
# Flask app
app = Flask(__name__)

block = BlockChain()


@app.route('/')
def index():
    return "Welcome to Blockchain"


@app.route("/chain", methods=["GET"])
def chain():
    response = {
        "chain": block.chains,
        "length": len(block.chains)
    }
    return jsonify(response), 200


@app.route("/is_valid", methods=["GET"])
def isValid():
    is_valid = block.is_valid_chain(block.chains)
    response = {}
    if is_valid:
        response = {
            "message": "The blockchain is valid."
        }
    else:
        response = {
            "message": "The blockchain is not valid."
        }

    return jsonify(response), 200


@app.route("/mine", methods=["POST"])
def mine():
    data = request.get_json()
    required = ['owner', 'Reg_no']
    if not all(key in data for key in required):
        return "Missing values", 400
    previous_block = block.previous_block()
    previous_proof = previous_block['proof']
    print("previous_proof", previous_proof)
    proof = block.proof_of_work(previous_proof)
    previous_hash = block.hash(previous_block)
    block.createBlock(owner=data['owner'], Reg_no=data['Reg_no'],
                      proof=proof, prev_hash=previous_hash)
    response = {
        "message": "New block created",
        "index": previous_block['index']+1,
        "owner": data['owner'],
        "Reg_no": data['Reg_no'],
        "proof": proof,
        "previous_hash": previous_hash
    }
    return jsonify(response), 200


app.run(debug=True, port=5000)

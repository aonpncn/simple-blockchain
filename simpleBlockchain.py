import datetime
import json         
import hashlib   
from flask import Flask, jsonify


class Blockchain:

    def __init__(self):

        # Collect group of Block
        self.chain = []

        # Collect the amount
        self.transaction = 0

        # Genesis Block
        self.create_block(nonce=1,previous_hash="0")



    # Create Block
    def create_block(self,nonce,previous_hash):  
        block={
            "index"         :len(self.chain)+1,                           
            "timestamp"     :str(datetime.datetime.now()),  
            "nonce"         :nonce,                         
            "data"          :self.transaction,                         
            "previous_hash" :previous_hash                  
        }
        self.chain.append(block)    
        return block               
    


    # Get previous block
    def get_previous_block(self):
        return self.chain[-1]



    # Encrypt Block
    def hash(self,block):
        encode_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()



    # PoW
    def proof_of_work(self,previous_nonce):      

        new_nonce = 1           
        check_proof = False     

        # Solve math problems
        while check_proof is False:

            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1

        return new_nonce
    


    # Check Block
    def is_chain_valid(self,chain):

        previous_block = chain[0]
        block_index = 1 

        # Check every block in chain
        while block_index<len(chain):
        
            # Case 1: Check Hash
            block = chain[block_index]

            if block["previous_hash"] != self.hash(previous_block):
                return False

            # Case 2: Check Nonce
            previous_nonce = previous_block["nonce"]  
            nonce = block["nonce"]                                                            
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()

            if hash_operation[:4] != "0000":
                return False
            

            previous_block = block   
            block_index += 1       

        return True
  

      

# Create Web Server
app = Flask(__name__)

# Activate Blockchain
blockchain = Blockchain()



@app.route('/')
def hello():
    return "<h1>Hello Blockchain</h1>"



@app.route('/get_chain', methods=["GET"])
def get_chain():
    responce={
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(responce),200           



# Mining
@app.route('/mining', methods=["GET"])
def mining_block():

    amount = 1000000    
    blockchain.transaction = blockchain.transaction + amount   
    
    # PoW
    previous_block = blockchain.get_previous_block()       
    previous_nonce = previous_block["nonce"]                
    nonce = blockchain.proof_of_work(previous_nonce)        
    # hash of previous block
    previous_hash = blockchain.hash(previous_block)         
    # update block
    block = blockchain.create_block(nonce,previous_hash)    
    # response
    response={
        "message"           :"Mining Block เรียบร้อย",
        "index"             :block["index"],
        "timestamp"         :block["timestamp"],
        "nonce"             :block["nonce"],
        "data"              :block["data"],
        "previous_hash"     :block["previous_hash"]
    }
    return jsonify(response),200



# Check Block
@app.route('/is_valid', methods=["GET"])
def is_valid():

    is_valid = blockchain.is_chain_valid(blockchain.chain)
    
    if is_valid:
        response = {"Message"   :"Blockchain is valid"}
    else:
        response = {"Message"   :"Have problem, Blockchain is not valid"}
    return jsonify(response), 200





# Run Server
if __name__ == "__main__":
    app.run()
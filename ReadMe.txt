

CONSENSUS ALGORITHM USED = Proof Of Stake
****INSTRUCTIONS BEFORE RUNNING THE CODE*****
Before running, enter this command in the command prompt

pip install -r requirements.txt
then run the api.py
*********************************************


api.py:
    Contains all the api endpoints to access the blockchain functions. Uses Flask api to create api endpoints

blockchain.py:
    Contains all the blockchain functionalities.Also contains the validator class which has all the stake and stakeholder info.

node.py:
    Contains the class definition of network participants: Manufacturer, Client, Distributor. Each Node class has user_type,
    user_name, public-private keys, booleans for productReceived and productSent, product reference for the products present
    with the concerned node

product.py:
    Product class definition present here. Each product has its own history and id and name.


====>  blockchain functions:
*)create_block = creates block
*)stringify = creates a list of transactions as strings for hashing and storing in the block
*)get_previous_block = returns the previous block
*)add_atomic_transactions = adds the atomic transaction (sender -> receiver) instead of manufacturer->distributor->client
*)add_transactions = adds the compiled transactions for the block creation in the form of manufacturer->distributor->client
*)hash = hashes the block and returns the hash
*)is_chain_valid = checks the validity of the chain
*)is_block_valid = checks if the block is valid or not
*)consensus = chooses the miner and validators (using PoS) and then asks the miner to forge a block. The validators then
                checks the block's validity and then after approval adds the block into the chain, while getting the
                transaction fees to miner and validators
*)calculate_merkle_root = generates merkle root using the list of strings (stringified transactions). Uses recursion to generate merkle root
*)select_leader = chooses the miner using PoS and randomization biased to Stake
*)verify_atomic_transactions = verifies the atomic transactions with the product history using its id and checking if
                                there was any issue in SCM. If there is a successful transaction, then product_history would be of length 4,
                                while if its 3, then client is guaranteed to lie (we can cross-check by checking the client's product field).
                                Similarly, if there are 2 transactions but the status has been only updated twice, the distributor is lying
                                Alternatively, we can check it using the self.product at each nodes for finding the liar

====> api.py API endpoints (Each api starts with http://localhost:5000)

*)register a user = @app.route('/register', methods=['POST'])
*)show all users = @app.route('/show/nodes', methods=['GET'])
*)show all users' stake = @app.route('/show/stakes', methods=['GET'])
*)show the blockchain = @app.route('/show/blockchain', methods=['GET'])
*)Create a new product = @app.route('/add/product', methods=['POST']) (Has JSON body)
*)Show product info = @app.route('/show/product', methods=['GET']) (Has JSON body)
*)Add a new transaction (atomic) = @app.route('/transaction', methods=['POST']) (Has JSON body)
*)Verify all the transactions (atomic) = @app.route('/verify', methods=['GET'])
*)Show all the verified transactions (complete and incomplete) = @app.route('/show/transactions', methods=['GET'])
*)Show qr code for a given product id = @app.route('/show/qrcode', methods=['GET'])
*)Start the forging process (consensus and mining) = @app.route('/start/forging', methods=['GET'])
*)Is the chain valid ? = @app.route('/is/chain/valid', methods=['GET'])

Node functions
*)receive a product
*)send a product
*)custom serializer

Manufacturer node functions
*)add, send product to/from list

Product functions
*)set_status() = set current status of the product and update history accordingly
*)print_qr_code() = prints the qrcode which displays the info about where it is present
*)to_dict = custom serializer

Adding atomic transaction
We are using custom node function to simulate the product behaviour. Like, manufacturer sends, distributor receives.
Then, distributor sends and client receives. So, for that, each node has its send and receive functions, which also updates the product's history,
to simulate it. To generate faulty transactions (lying case), we can manipulate the setting of the status, so that we know
the liar by checking is they have the product or not

Atomic transactions and verification => transaction
To simplify the SCM and to know the faulted, we can break a multi hand transaction to a manufacturer
to distributor and distributor to client. In this way, we can check where the product currently is. Once we find out
the product status and check the transaction and history, we can find who lied or the transaction was legit.
Thus, if found lying, the part of the stake is decreased of the liar as a part of penalty
All the verified transactions are then added to the final transaction list, for block creation.

STRUCTURES:
BLOCK:
    INDEX
    TIMESTAMP
    MINER
    PREVIOUS_HASH
    TRANSACTIONS (LIST)
    MERKLE_ROOT

TRANSACTION:
    TYPE: (COMPLETE OR INCOMPLETE)  {Incomplete = product hasn't reached the client}
    PRODUCT: Product name
    MANUFACTURER
    DISTRIBUTOR
    CLIENT
    TIMESTAMP
    DISTRIBUTOR_RECEIVED_AT
    DISTRIBUTOR_DISPATCHED_AT
    CLIENT_RECEIVED_AT

NODE/USER:
    USER_TYPE
    USER_NAME
    PUBLIC, PRIVATE KEYS
    bool PRODUCT_RECEIVED
    bool PRODUCT_SENT
    PRODUCT : Product present with the node

PRODUCT:
    PRODUCT_ID
    PRODUCT_NAME
    PRODUCT_HISTORY



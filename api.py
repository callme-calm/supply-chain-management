# backend/api.py

from flask import Flask, request, jsonify

from blockchain import Blockchain
from node import Node, ManufacturerNode

from product import Product
from datetime import datetime

blockchain = Blockchain()

app = Flask(__name__)

product_counter = 0

active_users = []
user_public_key = {}
products = []

"""
Retrieves the base users from the database.
This function queries the database to fetch the base users and returns them as a list.
"""


def base_users():
    users = [
        {"user_type": "manufacturer", "username": "manufacturer1", "security_deposit": 5000},
        {"user_type": "client", "username": "client123", "security_deposit": 1000},
        {"user_type": "client", "username": "client456", "security_deposit": 1500},
        {"user_type": "client", "username": "client789", "security_deposit": 2000},
        {"user_type": "distributor", "username": "distributor1", "security_deposit": 3000},
        {"user_type": "distributor", "username": "distributor2", "security_deposit": 2500},
        {"user_type": "distributor", "username": "distributor3", "security_deposit": 3500}

    ]
    for user in users:
        if user['user_type'] == 'manufacturer':
            active_users.append(ManufacturerNode(user['user_type'], user['username']))
        else:
            active_users.append(Node(user['user_type'], user['username']))
        blockchain.validator.add_stake(active_users[-1], user['security_deposit'])
        user_public_key[user['username']] = active_users[-1].public_key

    print("Added users")
    for user in active_users:
        print(user)

    stakeholders = blockchain.validator.show_all_stakes()
    for stakeholder, stake in stakeholders.items():
        print(stakeholder.user_name, stake)


"""
Retrieves the base products from the database.
This function queries the database to fetch the base products and returns them as a list.
"""


def base_products():
    global product_counter
    products_list = [
        {'product_name': 'First Product'},
        {'product_name': 'Second Product'},
        {'product_name': 'Third Product'},
        {'product_name': 'Fourth Product'},
        {'product_name': 'Fifth Product'}
    ]

    for product in products_list:
        products.append(
            Product(product_counter, product['product_name'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    active_users[0]))
        active_users[0].add_products(products[-1])
        product_counter += 1
    print("Added products")
    serialized_products = [product.to_dict() for product in products]
    print(serialized_products)

    for user in active_users:
        print(user)


"""
Registers a new user with the given username and password.
This function creates a new user account in the system using the provided username and password.
"""


@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    user_type = data.get('user_type')
    username = data.get('username')
    security_deposit = data.get('security_deposit')

    # Check if the user already exists

    for user in active_users:
        if user.user_name == username:
            return jsonify({"error": "User already exists"}), 400

    # Store user information

    active_users.append(Node(user_type, username))
    blockchain.validator.add_stake(active_users[-1], security_deposit)
    user_public_key[username] = active_users[-1].public_key

    return jsonify({"message": "User registered successfully"}), 201


""""
Displays the nodes in the system.
This function retrieves the nodes in the system and prints them to the console or displays them in the user interface.
"""


@app.route('/show/nodes', methods=['GET'])
def show_nodes():
    list_of_users = []
    for user in active_users:
        list_of_users.append(str(user))
    return jsonify(list_of_users)


"""
Displays the stakes of all users in the system.
This function retrieves the stakes of all users and prints them to the console or displays them in the user interface.
"""


@app.route('/show/stakes', methods=['GET'])
def show_stakes():
    stakeholders = blockchain.validator.show_all_stakes()
    stakeholder_data = [{"name": stakeholder.user_name, "stake": stake} for stakeholder, stake in stakeholders.items()]
    return jsonify(stakeholder_data)


""" 
Displays the blockchain. 
This function retrieves the blockchain and prints it to the console or displays it in the user interface.
"""


@app.route('/show/blockchain', methods=['GET'])
def show_blockchain():
    return jsonify(blockchain.chain)


"""
Creates a new product with the given name and price.
This function adds a new product to the system using the provided name and price.
"""


@app.route('/add/product', methods=['POST'])
def create_product():
    global product_counter
    global products
    old_size = len(products)
    product_name = request.json['product_name']
    products.append(
        Product(product_counter, product_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), active_users[0]))
    product_counter += 1
    if len(products) > old_size:
        return jsonify({"message": "Product added successfully"}), 201
    else:
        return jsonify({'error': 'Product not added'}), 400


@app.route('/show/product', methods=['GET'])
def show_product():
    global products
    serialized_products = [product.to_dict() for product in products]
    return jsonify(serialized_products)


"""
Adds a new transaction to the system.
This function creates a new transaction with the provided sender, recipient, and amount, and adds it to the system.
"""


@app.route('/transaction', methods=['POST'])
def add_transaction():
    global products
    data = request.json
    sender = data['sender']
    receiver = data['receiver']
    product_id = int(data['product_id'])
    fault_type = int(data.get('fault_type', 0))

    product = None
    flag = False
    user_sender = None
    user_receiver = None
    for p_it in products:
        if p_it.product_id == product_id:
            product = p_it
            print(product.product_name)
            flag = True
            break
    for iterator in active_users:
        if not user_sender and iterator.user_name == sender:
            print("Sender found")
            user_sender = iterator
        elif not user_receiver and iterator.user_name == receiver:
            print("Receiver found")
            user_receiver = iterator
    if not user_sender and not user_receiver:
        flag = False

    if flag:
        success = blockchain.add_atomic_transaction(user_sender, user_receiver, product, fault_type)
        if success:
            return jsonify({"message": "transaction successfully"}), 201
        else:
            return jsonify({"error": "Could not proceed with transaction, distributor is busy"}), 400
    else:
        return jsonify({"error": "product doesn't exists"}), 400


@app.route('/verify', methods=['GET'])
def verify():
    blockchain.verify_atomic_transaction()
    return jsonify({"message": "verified"}), 200


@app.route('/show/transactions', methods=['GET'])
def show_verified_transactions():
    return jsonify(blockchain.transactions), 200


"""
Displays a QR code representing the given data.
This function generates a QR code image based on the provided data and displays it to the user.
"""


@app.route('/show/qrcode', methods=['GET'])
def show_qr_code():
    data = request.json
    product_id = data['product_id']
    if product_id > len(products):
        return jsonify({'error': 'This product does not exist'}), 400
    product = products[product_id]
    flag = product.print_qr_code()
    if not flag:
        return jsonify({"Error": " in generating qrcode for the product"}), 400

    return jsonify({"message": "qrcode generated successfully"})


"""
Starts the forging process to create new blocks on the blockchain.
This function initiates the process of forging by which new blocks are created and added to the blockchain.
"""


@app.route('/start/forging', methods=['GET'])
def start_forging():
    blockchain.verify_atomic_transaction()
    fault = request.json['fault']
    message = blockchain.consensus(fault)
    if not message:
        return jsonify({'Error': 'Consensus was not reached or the block was not forged'}), 400
    return jsonify({'message': 'Hash of the block created'}), 200


# Checks if the blockchain is valid

@app.route('/is/chain/valid', methods=['GET'])
def is_chain_valid():
    if blockchain.is_chain_valid():
        return jsonify({'message': 'The blockchain is valid'})
    else:
        return jsonify({'Error': 'The blockchain is not valid'}), 400


if __name__ == '__main__':
    base_users()
    base_products()
    app.run(port=5000, debug=True)

import requests

# Define user data for clients, distributors, and manufacturer
transactions = [
    {'sender': 'manufacturer1', 'receiver': 'distributor1', 'product_id': '0'},
    {'sender': 'manufacturer1', 'receiver': 'distributor2', 'product_id': '2'},
    {'sender': 'manufacturer1', 'receiver': 'distributor1', 'product_id': '2'},
    {'sender': 'distributor1', 'receiver': 'client123', 'product_id': '0'},
    # {'sender': 'distributor1', 'receiver': 'client123', 'product_id': '0', 'fault_type': '1'},
    # {'sender': 'distributor1', 'receiver': 'client123', 'product_id': '0', 'fault_type': '2'},
    # {'sender': 'distributor2', 'receiver': 'client123', 'product_id': '1'},
    # {'sender': 'distributor1', 'receiver': 'client456', 'product_id': '0'},
]

# URL of the registration endpoint
transaction_url = "http://localhost:5000/transaction"

verify_url = "http://localhost:5000/verify"
# Loop through user data and send registration requests


for transaction in transactions:
    response = requests.post(transaction_url, json=transaction)
    if response.status_code == 201:
        print(f' ${transaction} registered successfully.')
    else:
        print(f"Error registering {transaction}: {response.status_code}")
        print(response.json())

# requests.get()

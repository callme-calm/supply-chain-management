import requests

products = [
    {'product_name': 'First Product'},
    {'product_name': 'Second Product'},
    {'product_name': 'Third Product'},
    {'product_name': 'Fourth Product'},
    {'product_name': 'Fifth Product'}
]
add_product_url = "http://localhost:5000/add/product"

for product in products:
    response = requests.post(add_product_url, json=product)
    if response.status_code == 201:
        print(f"Product {product['product_name']} added successfully")
    else:
        print(f"Error registering product {product['product_name']}: {response.status_code}")


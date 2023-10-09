import requests

nodes = requests.get("http://localhost:5000/show/nodes").json()
for node in nodes:
    print(node)

# print(requests.get("http://localhost:5000/show/stakes").json())
#
# requests.get("http://localhost:5000/verify")
# #
# print(requests.get("http://localhost:5000/show/stakes").json())
# #
# print(requests.get("http://localhost:5000/show/transactions").json())
#
# print(requests.get("http://localhost:5000/start/forging", json={'fault': None}).json())
#
# print(requests.get("http://localhost:5000/show/transactions").json())
#
# blocks = requests.get("http://localhost:5000/show/blockchain").json()
# for block in blocks:
#     print(block)

# product_ids = [
#     {'product_id': 0},
#     {'product_id': 1},
#     {'product_id': 2},
#     {'product_id': 0}
# ]
#
# for pro in product_ids:
#     requests.get("http://localhost:5000/show/qrcode", json=pro)

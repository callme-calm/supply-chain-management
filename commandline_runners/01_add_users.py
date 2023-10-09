import requests

# Define user data for clients, distributors, and manufacturer
users = [
    {"user_type": "client", "username": "client123", "security_deposit": 1000},
    {"user_type": "client", "username": "client456", "security_deposit": 1500},
    {"user_type": "client", "username": "client789", "security_deposit": 2000},
    {"user_type": "distributor", "username": "distributor1", "security_deposit": 3000},
    {"user_type": "distributor", "username": "distributor2", "security_deposit": 2500},
    {"user_type": "distributor", "username": "distributor3", "security_deposit": 3500},
    {"user_type": "manufacturer", "username": "manufacturer1", "security_deposit": 5000}
]

# URL of the registration endpoint
registration_url = "http://localhost:5000/register"

# Loop through user data and send registration requests
for user in users:
    response = requests.post(registration_url, json=user)
    if response.status_code == 201:
        print(f"User {user['username']} registered successfully.")
    else:
        print(f"Error registering user {user['username']}: {response.status_code}")

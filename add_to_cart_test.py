import requests
import json

# API endpoint
url = "https://ojt-stub-server.onrender.com/cart/add"

# Your token
token = "gfhfgdf"

# Product details (Western Dress)
cart_item = {
    "productId": "2013",
    "productName": "Western Dress",
    "price": 1800,
    "quantity": 1,
    "size": "M",
    "color": "Black"
}

# Make POST request
response = requests.post(
    url,
    params={"token": token},
    json=cart_item,
    headers={"Content-Type": "application/json"}
)

# Print response
print("Status Code:", response.status_code)
print("\nResponse:")
print(json.dumps(response.json(), indent=2))

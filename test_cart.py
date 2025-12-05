import requests
import json

BASE_URL = "https://ojt-stub-server.onrender.com"
TOKEN = "gfhfgdf"

print("=" * 50)
print("  CART TESTING - HTTP STUB SERVER")
print("=" * 50)

# Step 1: Add item to cart
print("\n[1] Adding Western Dress to cart...")
add_response = requests.post(
    f"{BASE_URL}/cart/add",
    params={"token": TOKEN},
    json={
        "productId": "2013",
        "productName": "Western Dress",
        "price": 1800,
        "quantity": 1,
        "size": "M",
        "color": "Black"
    }
)

print(f"Status: {add_response.status_code}")
print("Response:")
print(json.dumps(add_response.json(), indent=2))

# Step 2: View cart
print("\n" + "=" * 50)
print("[2] Viewing cart contents...")
cart_response = requests.get(
    f"{BASE_URL}/cart",
    params={"token": TOKEN}
)

print(f"Status: {cart_response.status_code}")
print("Response:")
print(json.dumps(cart_response.json(), indent=2))

print("\n" + "=" * 50)
print("✅ Cart test complete!")
print("=" * 50)

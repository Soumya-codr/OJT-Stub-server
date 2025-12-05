import requests
import json

# Use local server for testing
BASE_URL = "http://localhost:5600"
TOKEN = "test123"

print("=" * 60)
print("  REAL CART TESTING - In-Memory Storage")
print("=" * 60)

# Test 1: Add Western Dress
print("\n[1] Adding Western Dress to cart...")
response1 = requests.post(
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
print(f"Status: {response1.status_code}")
print(json.dumps(response1.json(), indent=2))

# Test 2: Add another item
print("\n" + "=" * 60)
print("[2] Adding Men's Sweater to cart...")
response2 = requests.post(
    f"{BASE_URL}/cart/add",
    params={"token": TOKEN},
    json={
        "productId": "101",
        "productName": "Men's Winter Sweater",
        "price": 700,
        "quantity": 2,
        "size": "L",
        "color": "Blue"
    }
)
print(f"Status: {response2.status_code}")
print(json.dumps(response2.json(), indent=2))

# Test 3: View cart (should show BOTH items now!)
print("\n" + "=" * 60)
print("[3] Viewing cart (should show both items)...")
response3 = requests.get(
    f"{BASE_URL}/cart",
    params={"token": TOKEN}
)
print(f"Status: {response3.status_code}")
print(json.dumps(response3.json(), indent=2))

# Test 4: Clear cart
print("\n" + "=" * 60)
print("[4] Clearing cart...")
response4 = requests.post(
    f"{BASE_URL}/cart/clear",
    params={"token": TOKEN}
)
print(f"Status: {response4.status_code}")
print(json.dumps(response4.json(), indent=2))

# Test 5: View empty cart
print("\n" + "=" * 60)
print("[5] Viewing cart after clear (should be empty)...")
response5 = requests.get(
    f"{BASE_URL}/cart",
    params={"token": TOKEN}
)
print(f"Status: {response5.status_code}")
print(json.dumps(response5.json(), indent=2))

print("\n" + "=" * 60)
print("✅ Real cart testing complete!")
print("=" * 60)

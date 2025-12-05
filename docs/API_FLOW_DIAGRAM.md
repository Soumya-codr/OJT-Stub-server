# 🔄 API Flow Diagram - E-Commerce Stub Server

## 📊 Complete User Journey

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REGISTRATION                         │
│  POST /register                                              │
│  ➜ Get Token: "xyz789abc"                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    BROWSE CATEGORIES                         │
│  GET /categories?token=xyz789abc                            │
│  ➜ See: Electronics, Clothing, TV, Smartphones, etc.        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  SELECT CATEGORY (e.g., Clothing)           │
│  GET /categories/2?token=xyz789abc                          │
│  ➜ See: Men's Clothing, Women's Clothing                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              SELECT SUBCATEGORY (e.g., Women's)             │
│  GET /categories/2/subcategories/2?token=xyz789abc          │
│  ➜ See: Dresses, Tops, Jeans, Accessories                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  VIEW PRODUCT DETAILS                        │
│  GET /categories/2/subcategories/2/products/2013            │
│      ?token=xyz789abc                                        │
│  ➜ See: Western Dress - ₹1800, Images, Delivery Info        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    ADD TO CART ⭐                            │
│  POST /cart/add?token=xyz789abc                             │
│  Body: {productId, name, price, quantity, size, color}      │
│  ➜ Success: "Item added to cart successfully!"              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      VIEW CART                               │
│  GET /cart?token=xyz789abc                                  │
│  ➜ See: All items, Subtotal, Tax, Total                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     PLACE ORDER                              │
│  POST /order/place?token=xyz789abc                          │
│  Body: {name, email, address, payment, items}               │
│  ➜ Get: Order ID, Tracking ID, Estimated Delivery           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    TRACK ORDER                               │
│  GET /order/ORD123456?token=xyz789abc                       │
│  ➜ See: Order status, Tracking history, Delivery date       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛒 Cart Flow (Detailed)

```
START
  │
  ├─► Register/Login
  │   └─► Get Token
  │
  ├─► Browse Products
  │   ├─► Categories
  │   ├─► Subcategories
  │   └─► Product Details
  │
  ├─► ADD TO CART ⭐
  │   │
  │   ├─► POST /cart/add
  │   │   ├─► Send: productId, name, price, quantity
  │   │   └─► Receive: Success message + Cart total
  │   │
  │   └─► GET /cart
  │       └─► View all cart items
  │
  ├─► Place Order
  │   └─► POST /order/place
  │       └─► Get Order ID
  │
  └─► Track Order
      └─► GET /order/:orderId
          └─► See delivery status
```

---

## 🔐 Authentication Flow

```
┌──────────────┐
│   No Token   │
└──────┬───────┘
       │
       ├─► Try to access /categories
       │   └─► ❌ 401 Unauthorized
       │       └─► "Please login first!"
       │
       ├─► POST /register
       │   └─► ✅ Get Token: "xyz789abc"
       │
       └─► Access /categories?token=xyz789abc
           └─► ✅ 200 Success
               └─► See all categories
```

---

## 📦 Product Discovery Flow

```
/categories
    │
    ├─► Category 1: Electronics
    │   ├─► Subcategory 1.1: Laptops
    │   │   ├─► Product 1001: Dell Inspiron
    │   │   ├─► Product 1002: HP Pavilion
    │   │   └─► Product 1003: Lenovo ThinkPad
    │   │
    │   └─► Subcategory 1.2: Smartphones
    │       ├─► Product 1101: iPhone 15
    │       └─► Product 1102: Samsung Galaxy
    │
    └─► Category 2: Clothing Store
        ├─► Subcategory 2.1: Men's Clothing
        │   ├─► Product 2001: T-Shirt
        │   └─► Product 2002: Jeans
        │
        └─► Subcategory 2.2: Women's Clothing
            ├─► Product 2013: Western Dress ⭐
            └─► Product 2014: Kurti
```

---

## 🎯 Cart Operations

```
CART OPERATIONS
│
├─► ADD ITEM
│   POST /cart/add
│   ├─► Input: Product details
│   └─► Output: Updated cart total
│
├─► VIEW CART
│   GET /cart
│   ├─► Output: All items
│   └─► Output: Summary (subtotal, tax, total)
│
└─► CHECKOUT
    POST /order/place
    ├─► Input: Shipping details
    └─► Output: Order confirmation
```

---

## 🔄 Request-Response Cycle

```
CLIENT                          SERVER
  │                               │
  ├─► POST /cart/add ────────────►│
  │   + Token                     │
  │   + Product Data              │
  │                               │
  │                          ┌────┴────┐
  │                          │ Validate│
  │                          │  Token  │
  │                          └────┬────┘
  │                               │
  │                          ┌────┴────┐
  │                          │ Process │
  │                          │Template │
  │                          └────┬────┘
  │                               │
  │◄──── Response (JSON) ─────────┤
  │   + Success message           │
  │   + Cart item details         │
  │   + Cart total                │
  │                               │
```

---

## 📱 HTTP Methods Used

```
GET     ➜ Retrieve data (categories, products, cart, orders)
POST    ➜ Create/Add data (register, login, add to cart, place order)
PUT     ➜ Update data (not used in current version)
DELETE  ➜ Remove data (not used in current version)
```

---

## 🎨 Response Status Codes

```
200 ✅ Success          - Request successful
201 ✅ Created          - Resource created (register, order)
400 ❌ Bad Request      - Invalid data sent
401 ❌ Unauthorized     - Token missing/invalid
404 ❌ Not Found        - Endpoint/Resource doesn't exist
500 ❌ Server Error     - Internal server error
```

---

## 🚀 Quick Test Path

```
1. Register        ➜ Get Token
2. Categories      ➜ See all categories
3. Category 2      ➜ Clothing Store
4. Subcategory 2   ➜ Women's Clothing
5. Product 2013    ➜ Western Dress details
6. Add to Cart     ➜ POST with product data ⭐
7. View Cart       ➜ Verify item added
8. Place Order     ➜ Complete purchase
9. Track Order     ➜ Check delivery status
```

---

## 🎯 Testing Priority

```
Priority 1 (Must Test):
├─► Register/Login
├─► View Categories
├─► Add to Cart ⭐
└─► View Cart

Priority 2 (Should Test):
├─► View Products
├─► Product Details
└─► Place Order

Priority 3 (Nice to Test):
├─► Search Products
├─► View Profile
└─► Track Order
```

---

**Use this diagram as reference while testing! 📊**

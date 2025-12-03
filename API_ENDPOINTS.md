# 🌐 Complete API Endpoints List

## All Available URLs for Testing

**Base URL:** `http://localhost:5600`

---

## 📋 **Quick Reference - All Endpoints**

### **1. Server Status**
```
GET http://localhost:5600/
```
**Response:** Server info and available endpoints

---

### **2. Authentication (No Token Required)**

#### **Register User**
```
POST http://localhost:5600/register

Body (JSON):
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "message": "User registered successfully",
  "userId": "a7b3c9d2e",
  "token": "x8y2z5k9m",
  "timestamp": "2025-12-03T10:30:00"
}
```

#### **Login User**
```
POST http://localhost:5600/login

Body (JSON):
{
  "email": "test@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "token": "x8y2z5k9m",
  "userId": "a7b3c9d2e",
  "timestamp": "2025-12-03T10:30:00"
}
```

---

### **3. Categories (Token Required)**

#### **Get All Categories**
```
GET http://localhost:5600/categories

Headers:
Authorization: your_token_here

Response:
{
  "categories": [
    {"id": 1, "name": "Electronics", "itemCount": 9},
    {"id": 2, "name": "Clothing", "itemCount": 9},
    {"id": 3, "name": "TV & Appliances", "itemCount": 9},
    {"id": 4, "name": "Smartphones", "itemCount": 9},
    {"id": 5, "name": "Kitchen", "itemCount": 9},
    {"id": 6, "name": "Home Decor", "itemCount": 9}
  ],
  "timestamp": "2025-12-03T10:30:00"
}
```

#### **Get Category Details**
```
GET http://localhost:5600/categories/1

Headers:
Authorization: your_token_here

Response:
{
  "categoryId": 1,
  "categoryName": "Electronics",
  "subcategories": [
    {"id": 1, "name": "Laptops", "itemCount": 3},
    {"id": 2, "name": "Headphones", "itemCount": 3},
    {"id": 3, "name": "Cameras", "itemCount": 3}
  ],
  "timestamp": "2025-12-03T10:30:00"
}
```

**All Category IDs:**
- `1` - Electronics
- `2` - Clothing
- `3` - TV & Appliances
- `4` - Smartphones
- `5` - Kitchen
- `6` - Home Decor

---

### **4. Products (Token Required)**

#### **Get Products in Subcategory**
```
GET http://localhost:5600/categories/1/subcategories/1

Headers:
Authorization: your_token_here

Response:
{
  "categoryId": 1,
  "subcategoryId": 1,
  "subcategoryName": "Laptops",
  "products": [
    {
      "id": 1001,
      "name": "Dell Inspiron 15",
      "price": 45000,
      "rating": 4.5,
      "inStock": true,
      "specs": "Intel i5, 8GB RAM, 512GB SSD"
    },
    // ... more products
  ],
  "totalProducts": 3,
  "timestamp": "2025-12-03T10:30:00"
}
```

**Popular Product URLs:**
```
Electronics → Laptops:
GET http://localhost:5600/categories/1/subcategories/1

Electronics → Headphones:
GET http://localhost:5600/categories/1/subcategories/2

Electronics → Cameras:
GET http://localhost:5600/categories/1/subcategories/3

Clothing → Men:
GET http://localhost:5600/categories/2/subcategories/1

Clothing → Women:
GET http://localhost:5600/categories/2/subcategories/2

Smartphones → Android:
GET http://localhost:5600/categories/4/subcategories/1

Smartphones → iPhone:
GET http://localhost:5600/categories/4/subcategories/2
```

#### **Get Single Product Details**
```
GET http://localhost:5600/categories/1/subcategories/1/products/1001

Headers:
Authorization: your_token_here

Response:
{
  "productId": 1001,
  "name": "Dell Inspiron 15",
  "price": 45000,
  "rating": 4.5,
  "inStock": true,
  "specs": "Intel i5, 8GB RAM, 512GB SSD",
  "description": "Premium quality Dell Inspiron 15...",
  "images": ["dell_inspiron_15_1.jpg", "dell_inspiron_15_2.jpg"],
  "deliveryInfo": {
    "estimatedDays": "3-5 days",
    "freeDelivery": true,
    "returnPolicy": "7 days return"
  },
  "timestamp": "2025-12-03T10:30:00"
}
```

---

### **5. Shopping Cart (Token Required)**

#### **Add to Cart**
```
POST http://localhost:5600/cart/add

Headers:
Authorization: your_token_here

Body (JSON):
{
  "productId": 1001,
  "quantity": 2
}

Response:
{
  "success": true,
  "message": "Product added to cart",
  "cartId": "cart_x7y2z5",
  "timestamp": "2025-12-03T10:30:00"
}
```

#### **View Cart**
```
GET http://localhost:5600/cart

Headers:
Authorization: your_token_here

Response:
{
  "cartId": "cart_x7y2z5",
  "items": [
    {
      "productId": 1001,
      "name": "Dell Inspiron 15",
      "quantity": 2,
      "price": 45000,
      "total": 90000
    }
  ],
  "totalItems": 2,
  "totalAmount": 90000,
  "timestamp": "2025-12-03T10:30:00"
}
```

---

### **6. Orders (Token Required)**

#### **Place Order**
```
POST http://localhost:5600/order/place

Headers:
Authorization: your_token_here

Body (JSON):
{
  "cartId": "cart_x7y2z5",
  "address": "123 Main St, City",
  "paymentMethod": "COD"
}

Response (after 3 second delay):
{
  "success": true,
  "message": "Order placed successfully",
  "orderId": "ORD_a7b3c9d2e",
  "estimatedDelivery": "3-5 days",
  "timestamp": "2025-12-03T10:30:00"
}
```

#### **Get All Orders**
```
GET http://localhost:5600/orders

Headers:
Authorization: your_token_here

Response:
{
  "orders": [
    {
      "orderId": "ORD_a7b3c9d2e",
      "date": "2025-12-03",
      "status": "Processing",
      "total": 90000
    }
  ],
  "totalOrders": 1,
  "timestamp": "2025-12-03T10:30:00"
}
```

#### **Track Order**
```
GET http://localhost:5600/order/ORD_a7b3c9d2e

Headers:
Authorization: your_token_here

Response:
{
  "orderId": "ORD_a7b3c9d2e",
  "status": "Processing",
  "items": [...],
  "total": 90000,
  "estimatedDelivery": "3-5 days",
  "timestamp": "2025-12-03T10:30:00"
}
```

---

### **7. Search (Token Required)**

```
GET http://localhost:5600/search?q=laptop

Headers:
Authorization: your_token_here

Response:
{
  "query": "laptop",
  "results": [
    {
      "id": 1001,
      "name": "Dell Inspiron 15",
      "price": 45000,
      "category": "Electronics"
    }
  ],
  "totalResults": 1,
  "timestamp": "2025-12-03T10:30:00"
}
```

---

### **8. User Profile (Token Required)**

```
GET http://localhost:5600/profile

Headers:
Authorization: your_token_here

Response:
{
  "userId": "a7b3c9d2e",
  "name": "Test User",
  "email": "test@example.com",
  "orders": 5,
  "timestamp": "2025-12-03T10:30:00"
}
```

---

### **9. Logout (Token Required)**

```
POST http://localhost:5600/logout

Headers:
Authorization: your_token_here

Response:
{
  "success": true,
  "message": "Logged out successfully",
  "timestamp": "2025-12-03T10:30:00"
}
```

---

## 🧪 **Testing Flow (Complete Journey)**

### **Step 1: Register**
```
POST http://localhost:5600/register
Body: {"name": "John", "email": "john@test.com", "password": "pass123"}
```
**Copy the token from response!**

---

### **Step 2: Browse Categories**
```
GET http://localhost:5600/categories
Header: Authorization: your_token
```

---

### **Step 3: View Electronics**
```
GET http://localhost:5600/categories/1
Header: Authorization: your_token
```

---

### **Step 4: View Laptops**
```
GET http://localhost:5600/categories/1/subcategories/1
Header: Authorization: your_token
```

---

### **Step 5: View Product Details**
```
GET http://localhost:5600/categories/1/subcategories/1/products/1001
Header: Authorization: your_token
```

---

### **Step 6: Add to Cart**
```
POST http://localhost:5600/cart/add
Header: Authorization: your_token
Body: {"productId": 1001, "quantity": 1}
```

---

### **Step 7: View Cart**
```
GET http://localhost:5600/cart
Header: Authorization: your_token
```

---

### **Step 8: Place Order**
```
POST http://localhost:5600/order/place
Header: Authorization: your_token
Body: {"cartId": "cart_xxx", "address": "123 Main St", "paymentMethod": "COD"}
```
**Wait 3 seconds for response!**

---

### **Step 9: View Orders**
```
GET http://localhost:5600/orders
Header: Authorization: your_token
```

---

### **Step 10: Track Order**
```
GET http://localhost:5600/order/ORD_xxx
Header: Authorization: your_token
```

---

## 📱 **For Mobile Testing (ngrok)**

Replace `http://localhost:5600` with your ngrok URL:
```
https://abc123.ngrok-free.app/categories
https://abc123.ngrok-free.app/register
etc.
```

---

## 🎯 **Quick Copy-Paste URLs**

```
http://localhost:5600/
http://localhost:5600/register
http://localhost:5600/login
http://localhost:5600/categories
http://localhost:5600/categories/1
http://localhost:5600/categories/1/subcategories/1
http://localhost:5600/categories/1/subcategories/1/products/1001
http://localhost:5600/cart/add
http://localhost:5600/cart
http://localhost:5600/order/place
http://localhost:5600/orders
http://localhost:5600/order/ORD_123
http://localhost:5600/search?q=laptop
http://localhost:5600/profile
http://localhost:5600/logout
```

---

## ⚠️ **Important Notes**

1. **Token Required:** All endpoints except `/`, `/register`, `/login` need Authorization header
2. **Token Format:** Just paste the token value (no "Bearer" prefix needed)
3. **Delays:** Some endpoints have delays (categories: 400ms, products: 500ms, order: 3000ms)
4. **Product IDs:** Start from 1001, 1002, 1003, etc.
5. **Category IDs:** 1-6
6. **Subcategory IDs:** 1-3 per category

---

**Ye file save kar lo - demo ke liye perfect hai!** 📋✅

# 🧪 Complete API Testing Guide - HTTP Stub Server

## 📋 Base Information
- **Live Server URL:** `https://ojt-stub-server.onrender.com`
- **Test Token:** `test123` (use any random string)
- **Testing Tool:** Postman or cURL or Python script

---

## 🎯 Complete Testing Flow (Step-by-Step)

### **STEP 1: Register New User** 📝

**Method:** `POST`  
**URL:** `https://ojt-stub-server.onrender.com/register`

**Body (JSON):**
```json
{
  "name": "Soumya Sagar",
  "email": "soumya@example.com",
  "phone": "9876543210",
  "password": "password123"
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Account created successfully!",
  "user": {
    "id": "abc123xyz",
    "name": "Soumya Sagar",
    "email": "soumya@example.com",
    "phone": "9876543210"
  },
  "token": "xyz789abc"
}
```

**✅ Copy the `token` from response - you'll need it for next steps!**

---

### **STEP 2: Login (Optional)** 🔐

**Method:** `POST`  
**URL:** `https://ojt-stub-server.onrender.com/login`

**Body (JSON):**
```json
{
  "email": "soumya@example.com",
  "password": "password123",
  "name": "Soumya Sagar"
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Login successful!",
  "user": {
    "id": "abc123xyz",
    "email": "soumya@example.com",
    "name": "Soumya Sagar"
  },
  "token": "xyz789abc"
}
```

---

### **STEP 3: View All Categories** 📦

**Method:** `GET`  
**URL:** `https://ojt-stub-server.onrender.com/categories?token=YOUR_TOKEN_HERE`

**Example:**
```
https://ojt-stub-server.onrender.com/categories?token=xyz789abc
```

**Expected Response:**
```json
{
  "categories": [
    {"id": 1, "name": "Electronics", "icon": "electronics.png", "itemCount": 250},
    {"id": 2, "name": "Clothing Store", "icon": "clothing.png", "itemCount": 500},
    {"id": 3, "name": "TV & Appliances", "icon": "tv.png", "itemCount": 180}
  ]
}
```

---

### **STEP 4: View Category Subcategories** 🏷️

**Method:** `GET`  
**URL:** `https://ojt-stub-server.onrender.com/categories/2?token=YOUR_TOKEN_HERE`

**Example (Clothing Store):**
```
https://ojt-stub-server.onrender.com/categories/2?token=xyz789abc
```

**Expected Response:**
```json
{
  "categoryId": 2,
  "categoryName": "Clothing Store",
  "subcategories": [
    {"id": 1, "name": "Men's Clothing", "itemCount": 150},
    {"id": 2, "name": "Women's Clothing", "itemCount": 200}
  ]
}
```

---

### **STEP 5: View Products in Subcategory** 👗

**Method:** `GET`  
**URL:** `https://ojt-stub-server.onrender.com/categories/2/subcategories/2?token=YOUR_TOKEN_HERE`

**Example (Women's Clothing):**
```
https://ojt-stub-server.onrender.com/categories/2/subcategories/2?token=xyz789abc
```

**Expected Response:**
```json
{
  "categoryId": 2,
  "subcategoryId": 2,
  "subcategoryName": "Women's Clothing",
  "products": [
    {
      "id": 2013,
      "name": "Western Dress",
      "price": 1800,
      "originalPrice": 2500,
      "discount": "28% off",
      "rating": 4.4,
      "reviews": 892,
      "inStock": true,
      "image": "western_dress_1.jpg"
    }
  ]
}
```

---

### **STEP 6: View Single Product Details** 🔍

**Method:** `GET`  
**URL:** `https://ojt-stub-server.onrender.com/categories/2/subcategories/2/products/2013?token=YOUR_TOKEN_HERE`

**Example (Western Dress):**
```
https://ojt-stub-server.onrender.com/categories/2/subcategories/2/products/2013?token=xyz789abc
```

**Expected Response:**
```json
{
  "productId": 2013,
  "name": "Western Dress",
  "price": 1800,
  "originalPrice": 2500,
  "discount": "28% off",
  "rating": 4.4,
  "reviews": 892,
  "inStock": true,
  "description": "Premium quality Western Dress. High quality product.",
  "images": ["western_dress_1.jpg", "western_dress_2.jpg"],
  "deliveryInfo": {
    "estimatedDays": "3-5 days",
    "freeDelivery": true,
    "returnPolicy": "7 days return"
  }
}
```

---

### **STEP 7: Add Product to Cart** 🛒 ⭐ **MAIN STEP**

**Method:** `POST`  
**URL:** `https://ojt-stub-server.onrender.com/cart/add?token=YOUR_TOKEN_HERE`

**Example:**
```
https://ojt-stub-server.onrender.com/cart/add?token=xyz789abc
```

**Body (JSON):**
```json
{
  "productId": "2013",
  "productName": "Western Dress",
  "price": 1800,
  "quantity": 1,
  "size": "M",
  "color": "Black"
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Item added to cart successfully!",
  "cartItem": {
    "productId": "2013",
    "productName": "Western Dress",
    "price": "1800",
    "quantity": "1",
    "size": "M",
    "color": "Black"
  },
  "cartTotal": {
    "items": 1,
    "subtotal": "1800",
    "tax": 70,
    "total": 1870
  }
}
```

**✅ SUCCESS! Item added to cart!**

---

### **STEP 8: View Cart** 🛍️

**Method:** `GET`  
**URL:** `https://ojt-stub-server.onrender.com/cart?token=YOUR_TOKEN_HERE`

**Example:**
```
https://ojt-stub-server.onrender.com/cart?token=xyz789abc
```

**Expected Response:**
```json
{
  "cartId": "cart123xyz",
  "items": [
    {
      "productId": 101,
      "name": "Men's Winter Sweater",
      "price": 700,
      "quantity": 1,
      "size": "L",
      "color": "Black",
      "image": "sweater1.jpg"
    }
  ],
  "summary": {
    "subtotal": 700,
    "tax": 70,
    "deliveryCharges": 0,
    "discount": 0,
    "total": 770
  }
}
```

---

### **STEP 9: Place Order** 📦

**Method:** `POST`  
**URL:** `https://ojt-stub-server.onrender.com/order/place?token=YOUR_TOKEN_HERE`

**Example:**
```
https://ojt-stub-server.onrender.com/order/place?token=xyz789abc
```

**Body (JSON):**
```json
{
  "name": "Soumya Sagar",
  "email": "soumya@example.com",
  "phone": "9876543210",
  "address": "123 Main Street",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "productId": "2013",
  "productName": "Western Dress",
  "price": 1800,
  "quantity": 1,
  "size": "M",
  "paymentMethod": "COD",
  "totalAmount": 1870
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Your order has been placed successfully!",
  "orderId": "ORDabc123xyz",
  "orderDetails": {
    "customerName": "Soumya Sagar",
    "email": "soumya@example.com",
    "phone": "9876543210",
    "address": {
      "street": "123 Main Street",
      "city": "Mumbai",
      "state": "Maharashtra",
      "pincode": "400001"
    }
  },
  "estimatedDelivery": "3-5 business days",
  "trackingId": "TRKxyz789abc"
}
```

---

### **STEP 10: View All Orders** 📋

**Method:** `GET`  
**URL:** `https://ojt-stub-server.onrender.com/orders?token=YOUR_TOKEN_HERE`

**Example:**
```
https://ojt-stub-server.onrender.com/orders?token=xyz789abc
```

---

### **STEP 11: Track Specific Order** 🚚

**Method:** `GET`  
**URL:** `https://ojt-stub-server.onrender.com/order/ORD123456?token=YOUR_TOKEN_HERE`

**Example:**
```
https://ojt-stub-server.onrender.com/order/ORD123456?token=xyz789abc
```

---

## 🔧 Testing Methods

### **Method 1: Using Postman** (Recommended)

1. Open Postman
2. Create new request
3. Set method (GET/POST)
4. Paste URL
5. For POST requests:
   - Go to "Body" tab
   - Select "raw"
   - Select "JSON"
   - Paste JSON body
6. Click "Send"

---

### **Method 2: Using cURL (Command Line)**

**Add to Cart Example:**
```bash
curl -X POST "https://ojt-stub-server.onrender.com/cart/add?token=xyz789abc" ^
-H "Content-Type: application/json" ^
-d "{\"productId\":\"2013\",\"productName\":\"Western Dress\",\"price\":1800,\"quantity\":1,\"size\":\"M\",\"color\":\"Black\"}"
```

**View Cart Example:**
```bash
curl "https://ojt-stub-server.onrender.com/cart?token=xyz789abc"
```

---

### **Method 3: Using Python Script**

Run the provided `test_cart.py` script:
```bash
python test_cart.py
```

---

## 📝 Quick Test Checklist

- [ ] Register user and get token
- [ ] View categories
- [ ] View subcategories
- [ ] View products
- [ ] View product details
- [ ] **Add product to cart** ⭐
- [ ] View cart contents
- [ ] Place order
- [ ] View orders
- [ ] Track order

---

## 🎯 Quick Cart Test (Copy-Paste Ready)

**1. Register (POST):**
```
URL: https://ojt-stub-server.onrender.com/register
Body: {"name":"Test User","email":"test@example.com","phone":"9876543210","password":"test123"}
```

**2. Add to Cart (POST):**
```
URL: https://ojt-stub-server.onrender.com/cart/add?token=YOUR_TOKEN
Body: {"productId":"2013","productName":"Western Dress","price":1800,"quantity":1,"size":"M","color":"Black"}
```

**3. View Cart (GET):**
```
URL: https://ojt-stub-server.onrender.com/cart?token=YOUR_TOKEN
```

---

## ⚠️ Important Notes

1. **Token Required:** All endpoints (except register/login) need `?token=YOUR_TOKEN` in URL
2. **POST Requests:** Must have `Content-Type: application/json` header
3. **Response Time:** First request may take 30-60 seconds (Render cold start)
4. **Token Format:** Any string works (e.g., `test123`, `abc`, `mytoken`)

---

## 🐛 Troubleshooting

**Problem:** "Unauthorized" error  
**Solution:** Add `?token=YOUR_TOKEN` to URL

**Problem:** "Endpoint not found"  
**Solution:** Check URL spelling and method (GET/POST)

**Problem:** Slow response  
**Solution:** Wait 30-60 seconds for first request (Render cold start)

---

## 📞 Support

- GitHub: https://github.com/Soumya-codr/OJT-Stub-server
- Issues: https://github.com/Soumya-codr/OJT-Stub-server/issues

---

**Happy Testing! 🚀**

# 🛒 Cart Testing - Quick Guide

## 🚀 3-Step Cart Test

### **Step 1: Get Token** 
```
POST https://ojt-stub-server.onrender.com/register

Body:
{
  "name": "Your Name",
  "email": "your@email.com",
  "phone": "9876543210",
  "password": "test123"
}

✅ Copy the "token" from response!
```

---

### **Step 2: Add to Cart** ⭐
```
POST https://ojt-stub-server.onrender.com/cart/add?token=YOUR_TOKEN_HERE

Body:
{
  "productId": "2013",
  "productName": "Western Dress",
  "price": 1800,
  "quantity": 1,
  "size": "M",
  "color": "Black"
}

✅ Check response: "Item added to cart successfully!"
```

---

### **Step 3: View Cart**
```
GET https://ojt-stub-server.onrender.com/cart?token=YOUR_TOKEN_HERE

✅ You'll see your added item in the cart!
```

---

## 📱 Postman Setup (Screenshot Guide)

### **For POST Requests:**
1. Method: Select `POST`
2. URL: Paste the URL with `?token=YOUR_TOKEN`
3. Headers: Add `Content-Type: application/json`
4. Body: 
   - Click "Body" tab
   - Select "raw"
   - Select "JSON" from dropdown
   - Paste JSON body
5. Click "Send"

### **For GET Requests:**
1. Method: Select `GET`
2. URL: Paste the URL with `?token=YOUR_TOKEN`
3. Click "Send"

---

## 🎯 Real Example (Copy-Paste)

**Replace `YOUR_TOKEN_HERE` with actual token from Step 1!**

### Add Western Dress to Cart:
```
POST https://ojt-stub-server.onrender.com/cart/add?token=YOUR_TOKEN_HERE

Body:
{
  "productId": "2013",
  "productName": "Western Dress",
  "price": 1800,
  "quantity": 1,
  "size": "M",
  "color": "Black"
}
```

### Add Men's Sweater to Cart:
```
POST https://ojt-stub-server.onrender.com/cart/add?token=YOUR_TOKEN_HERE

Body:
{
  "productId": "101",
  "productName": "Men's Winter Sweater",
  "price": 700,
  "quantity": 2,
  "size": "L",
  "color": "Blue"
}
```

### Add Laptop to Cart:
```
POST https://ojt-stub-server.onrender.com/cart/add?token=YOUR_TOKEN_HERE

Body:
{
  "productId": "1001",
  "productName": "Dell Inspiron Laptop",
  "price": 45000,
  "quantity": 1,
  "size": "15.6 inch",
  "color": "Silver"
}
```

---

## 🔥 One-Line cURL Commands

**Register:**
```bash
curl -X POST "https://ojt-stub-server.onrender.com/register" -H "Content-Type: application/json" -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"phone\":\"9876543210\",\"password\":\"test123\"}"
```

**Add to Cart:**
```bash
curl -X POST "https://ojt-stub-server.onrender.com/cart/add?token=YOUR_TOKEN" -H "Content-Type: application/json" -d "{\"productId\":\"2013\",\"productName\":\"Western Dress\",\"price\":1800,\"quantity\":1,\"size\":\"M\",\"color\":\"Black\"}"
```

**View Cart:**
```bash
curl "https://ojt-stub-server.onrender.com/cart?token=YOUR_TOKEN"
```

---

## ✅ Success Indicators

**Add to Cart Success:**
```json
{
  "success": true,
  "message": "Item added to cart successfully!",
  "cartTotal": {
    "items": 1,
    "subtotal": "1800",
    "total": 1870
  }
}
```

**View Cart Success:**
```json
{
  "cartId": "xyz123",
  "items": [
    {
      "productId": 101,
      "name": "Men's Winter Sweater",
      "price": 700,
      "quantity": 1
    }
  ],
  "summary": {
    "subtotal": 700,
    "total": 770
  }
}
```

---

## ⚠️ Common Errors

**Error: "Unauthorized"**
```
❌ Problem: Token missing or invalid
✅ Solution: Add ?token=YOUR_TOKEN to URL
```

**Error: "Endpoint not found"**
```
❌ Problem: Wrong URL or method
✅ Solution: Check URL spelling and use POST for /cart/add
```

**Error: No response**
```
❌ Problem: Server cold start
✅ Solution: Wait 30-60 seconds and try again
```

---

## 🎓 Testing Checklist

- [ ] Open Postman
- [ ] Register user (POST /register)
- [ ] Copy token from response
- [ ] Add item to cart (POST /cart/add?token=...)
- [ ] Check success message
- [ ] View cart (GET /cart?token=...)
- [ ] Verify item is in cart
- [ ] Take screenshot for demo

---

**Done! Your cart is working! 🎉**

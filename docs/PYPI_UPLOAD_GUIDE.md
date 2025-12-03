# 📦 PyPI Upload Guide

## Quick Guide to Upload Your Package

---

## 🎯 Prerequisites

1. **PyPI Account**: https://pypi.org/account/register/
2. **Build Tools**: Already installed ✅

---

## 🚀 Upload Steps

### **Step 1: Build Package** (Already Done ✅)
```bash
python -m build
```

### **Step 2: Upload to PyPI**
```bash
python -m twine upload dist/*
```

Enter credentials when prompted:
- Username: your_pypi_username
- Password: your_pypi_password

---

## 🔐 Using API Token (Recommended)

1. Login to PyPI → Account Settings → API tokens
2. Create token and copy it
3. Upload with token:

```bash
python -m twine upload dist/* --username __token__ --password pypi-YOUR_TOKEN
```

---

## ✅ After Upload

**Install anywhere:**
```bash
pip install http-stub-server
```

**Run:**
```bash
http-stub-server
```

**Package URL:**
```
https://pypi.org/project/http-stub-server/
```

---

## 🎓 For Judges

> "Sir, maine ye project PyPI pe publish kiya hai. Koi bhi developer worldwide `pip install http-stub-server` karke use kar sakta hai!"

---

## ⚠️ Important

- Package name unique hona chahiye
- Agar taken hai toh `setup.py` mein name change karo
- Version update karne ke liye `setup.py` mein version number badhao

---

## 🐛 Common Errors

**"Package name exists"** → Change name in setup.py  
**"Invalid credentials"** → Use API token  
**"Version exists"** → Increase version number  

---

**That's it! Simple and straightforward.** 🚀

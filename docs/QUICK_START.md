# ⚡ Quick Start Guide

## Get Started in 3 Steps

---

## 🚀 Run the Server

### Option 1: From Package (Recommended)
```bash
pip install dist/http_stub_server-1.0.0-py3-none-any.whl
http-stub-server
```

### Option 2: From Source
```bash
python server.py
```

**Server URL:** http://localhost:5600

---

## 🧪 Test the API

```bash
# Test server
curl http://localhost:5600

# Register user
curl -X POST http://localhost:5600/register -H "Content-Type: application/json" -d "{\"name\":\"Test\",\"email\":\"test@test.com\",\"password\":\"pass123\"}"

# Login
curl -X POST http://localhost:5600/login -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"pass123\"}"
```

---

## 📚 Documentation

- **Main Docs:** [README.md](README.md)
- **PyPI Upload:** [PYPI_UPLOAD_GUIDE.md](PYPI_UPLOAD_GUIDE.md)
- **Demo Prep:** [docs/DEMO_CHECKLIST.md](docs/DEMO_CHECKLIST.md)
- **API Testing:** [docs/POSTMAN_TESTING_GUIDE.md](docs/POSTMAN_TESTING_GUIDE.md)

---

## 🎯 Key Features

- 60+ products catalog
- 15+ API endpoints
- Token-based authentication
- PyPI-ready package

---

**That's it! Simple and clean.** ✅

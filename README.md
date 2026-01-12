# 🚀 HTTP Stub Server - E-commerce API

A configurable mock API server for e-commerce testing and development, built with Python Flask.

**Published on PyPI:** https://pypi.org/project/http-stub-server/

---

## ⚡ Quick Start  

### Installation
```bash
# From PyPI (Recommended)
pip install http-stub-server

# Run the server
http-stub-server
```

### From Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

**Server URL:** http://localhost:5600

---

## 🎯 Features

✅ **15+ REST API Endpoints** - Complete e-commerce flow  
✅ **60+ Products** - 6 categories, 18 subcategories  
✅ **Token Authentication** - Simulated auth system  
✅ **Dynamic Routing** - Config-driven endpoints  
✅ **Template Variables** - `{{timestamp}}`, `{{randomId}}`, etc.  
✅ **Request Logging** - All API calls logged  
✅ **Hot Reload** - Config changes without restart  
✅ **CORS Enabled** - Frontend integration ready  
✅ **PyPI Package** - One-command installation  

---

## 📚 API Endpoints

### Authentication (No Token Required)
```
POST /register - Create account
POST /login    - User login
```

### Products (Token Required)
```
GET  /categories                                    - All categories
GET  /categories/:id                                - Category details
GET  /categories/:id/subcategories/:id              - Products list
GET  /categories/:id/subcategories/:id/products/:id - Product details
```

### Shopping (Token Required)
```
POST /cart/add     - Add to cart
GET  /cart         - View cart
POST /order/place  - Place order (3s delay)
GET  /orders       - Order history
GET  /order/:id    - Track order
```

**Complete API documentation:** [API_ENDPOINTS.md](API_ENDPOINTS.md)

---

## 🧪 Testing

### Automated Testing
```bash
python scripts\test_api.py
```

### Manual Testing
See [POSTMAN_TESTING_GUIDE.md](docs/POSTMAN_TESTING_GUIDE.md)

---

## 📊 Tech Stack

- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - Cross-origin support

---

## 📁 Project Structure

```
├── server.py              # Main Flask server (500+ lines)
├── data.py                # Product catalog (60+ products)
├── config.json            # API configuration
├── requirements.txt       # Dependencies
├── API_ENDPOINTS.md       # Complete API documentation
│
├── setup.py               # PyPI package config
├── pyproject.toml         # Modern packaging
├── MANIFEST.in            # File inclusion
├── LICENSE                # MIT License
│
├── docs/                  # Documentation
│   ├── CODE_SUMMARY_VIVA.md        # Code explanation for viva
│   ├── DEMO_CHECKLIST.md           # Demo preparation
│   ├── POSTMAN_TESTING_GUIDE.md    # API testing guide
│   ├── PPT_CONTENT.md              # Presentation content
│   ├── OJT_LOGBOOK_ENTRIES.md      # Backend logbook
│   └── OJT_LOGBOOK_FRONTEND.md     # Frontend logbook
│
└── scripts/               # Utility scripts
    ├── test_api.py        # Automated testing
    ├── install.bat        # Windows setup
    └── run.bat            # Quick start
```

---

## 🎓 For Students/Demo

Perfect for:
- ✅ Academic presentations
- ✅ API development learning
- ✅ Backend testing
- ✅ Postman demonstrations
- ✅ Frontend integration

**Demo Time:** 10-12 minutes  
**Difficulty:** Beginner-friendly  

---

## 📦 PyPI Package

**Package Name:** `http-stub-server`  
**Version:** 1.0.0  
**PyPI URL:** https://pypi.org/project/http-stub-server/

**Installation:**
```bash
pip install http-stub-server
```

**Usage:**
```bash
# Run on default port (5600)
http-stub-server

# Run on custom port
http-stub-server 8080

# Or set environment variable
PORT=8080 http-stub-server
```

---

## 🔧 Configuration

### Port Configuration
```bash
# Command line
http-stub-server 8080

# Environment variable
PORT=8080 http-stub-server

# config.json
{"port": 8080}
```

### Custom Endpoints
Edit `config.json` to add/modify endpoints. Server auto-reloads on changes.

---

## 📝 Logs

All API requests logged to: `logs/requests.log`

Each entry includes:
- Timestamp
- HTTP method
- URL path
- Status code
- Response time

---

## 🤝 Contributing

This is an academic project. Feel free to:
- Add more endpoints
- Enhance features
- Improve documentation

---

## 📄 License

MIT License - Free to use for learning and development

---

## 🆘 Documentation

- **API Endpoints:** [API_ENDPOINTS.md](API_ENDPOINTS.md)
- **Code Summary:** [docs/CODE_SUMMARY_VIVA.md](docs/CODE_SUMMARY_VIVA.md)
- **Demo Guide:** [docs/DEMO_CHECKLIST.md](docs/DEMO_CHECKLIST.md)
- **Testing Guide:** [docs/POSTMAN_TESTING_GUIDE.md](docs/POSTMAN_TESTING_GUIDE.md)

---

## 📊 Project Statistics

- **Lines of Code:** 900+
- **API Endpoints:** 15+
- **Products:** 60+
- **Categories:** 6
- **Subcategories:** 18
- **Documentation Files:** 7
- **Python Version:** 3.8+

---

## 🌟 Key Highlights

- 🌍 **Published on PyPI** - Worldwide accessible
- 📦 **One-Command Install** - `pip install http-stub-server`
- 🚀 **Production Ready** - Complete error handling
- 📚 **Well Documented** - Comprehensive guides
- 🧪 **Fully Tested** - Automated test suite
- 🎓 **Educational** - Perfect for learning

---

**Made with ❤️ for learning Python backend development**

**PyPI Package:** https://pypi.org/project/http-stub-server/

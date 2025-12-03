# 📚 Code Summary - Viva Preparation

## Complete Project Code Explanation

---

## 🎯 **Project Overview**

**Name:** HTTP Stub Server (E-commerce API Mock Server)  
**Language:** Python 3.8+  
**Framework:** Flask 3.0.0  
**Total Lines:** 900+ lines  
**Files:** 3 main files (server.py, data.py, config.json)  

---

## 📁 **File Structure**

```
server.py       → Main server code (500+ lines)
data.py         → Product catalog (60+ products)
config.json     → API configuration (15+ endpoints)
requirements.txt → Dependencies
setup.py        → PyPI package config
demo.html       → Mobile demo UI
```

---

## 🔧 **1. server.py - Main Server File**

### **Imports (Lines 1-20)**
```python
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json, time, re, datetime, random, string, os
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from data import category_data
```

**Explanation:**
- `Flask`: Web framework for creating API
- `CORS`: Allow frontend to access API
- `json`: Parse config.json and create responses
- `time`: Add delays for realistic simulation
- `datetime`: Generate timestamps
- `random/string`: Generate tokens and IDs
- `watchdog`: Monitor config.json for changes
- `data`: Import product catalog

---

### **Flask App Initialization (Lines 25-35)**
```python
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

CONFIG_PATH = 'config.json'
LOG_PATH = 'logs/requests.log'
config = {}
```

**Explanation:**
- Create Flask application
- Enable CORS for frontend integration
- Define file paths for config and logs
- Global variable to store configuration

---

### **Helper Functions**

#### **1. generate_random_id() (Lines 40-45)**
```python
def generate_random_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
```
**Purpose:** Generate unique IDs for users, orders  
**Example:** "a7b3c9d2e"  
**Used in:** Register, Login, Order placement  

---

#### **2. load_config() (Lines 50-60)**
```python
def load_config():
    global config
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print('✅ Configuration loaded successfully')
        return True
    except Exception as e:
        print(f'❌ Error loading config: {str(e)}')
        return False
```
**Purpose:** Load endpoints from config.json  
**Returns:** True/False  
**Called:** At startup and when config changes  

---

#### **3. log_request() (Lines 65-85)**
```python
def log_request(method, url, query_params, status_code, duration_ms):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'url': url,
        'query': query_params,
        'status': status_code,
        'duration': f'{duration_ms}ms'
    }
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')
```
**Purpose:** Log every API request to file  
**Logs:** Timestamp, method, URL, status, duration  
**File:** logs/requests.log  

---

#### **4. process_template() (Lines 90-130)**
```python
def process_template(obj, context):
    json_str = json.dumps(obj)
    
    # Replace {{timestamp}}
    json_str = json_str.replace('{{timestamp}}', datetime.now().isoformat())
    
    # Replace {{randomId}}
    while '{{randomId}}' in json_str:
        json_str = json_str.replace('{{randomId}}', generate_random_id(), 1)
    
    # Replace {{query.param}}
    for key, value in context.get('query', {}).items():
        placeholder = '{{query.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Replace {{body.field}}
    for key, value in context.get('body', {}).items():
        placeholder = '{{body.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    return json.loads(json_str)
```
**Purpose:** Replace template variables in responses  
**Variables:**
- `{{timestamp}}` → Current time
- `{{randomId}}` → Random ID
- `{{query.name}}` → URL parameter
- `{{body.email}}` → POST body field

**Example:**
```json
Input:  {"userId": "{{randomId}}", "time": "{{timestamp}}"}
Output: {"userId": "a7b3c9d2e", "time": "2025-12-03T10:30:00"}
```

---

#### **5. path_matches() (Lines 135-150)**
```python
def path_matches(endpoint_path, request_path):
    pattern = endpoint_path
    pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
    pattern = f'^{pattern}$'
    
    match = re.match(pattern, request_path)
    if match:
        return True, match.groupdict()
    return False, {}
```
**Purpose:** Match dynamic routes like `/order/:orderId`  
**Example:**
- Pattern: `/order/:orderId`
- Request: `/order/ORD123`
- Returns: `(True, {'orderId': 'ORD123'})`

---

### **Middleware Functions**

#### **1. before_request() (Lines 160-165)**
```python
@app.before_request
def before_request():
    request.start_time = time.time()
```
**Purpose:** Store request start time  
**Used for:** Calculating response duration  

---

#### **2. after_request() (Lines 170-185)**
```python
@app.after_request
def after_request(response):
    duration = int((time.time() - request.start_time) * 1000)
    log_request(request.method, request.path, dict(request.args), 
                response.status_code, duration)
    return response
```
**Purpose:** Log request after response sent  
**Calculates:** Response time in milliseconds  

---

### **Authentication**

#### **check_auth() (Lines 190-205)**
```python
def check_auth():
    token = request.headers.get('Authorization') or request.args.get('token')
    
    if not token:
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Please login first!',
            'redirectTo': '/register',
            'timestamp': datetime.now().isoformat()
        }), 401
    
    return None
```
**Purpose:** Check if user has valid token  
**Returns:** 401 error if no token, None if valid  
**Used in:** All protected routes  

---

### **API Endpoints**

#### **1. Home Endpoint (Lines 210-230)**
```python
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'HTTP Stub Server - Python Version',
        'status': 'running',
        'port': config.get('port', 5600),
        'version': '1.0.0',
        'endpoints': {...},
        'documentation': 'See README.md'
    })
```
**Purpose:** Server info and available endpoints  
**URL:** `GET /`  
**Auth:** Not required  

---

#### **2. Category Endpoint (Lines 235-270)**
```python
@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    category_key = str(category_id)
    if category_key not in category_data:
        return jsonify({'error': 'Category not found'}), 404
    
    category = category_data[category_key]
    subcategories = []
    for sub_id, sub_data in category['subcategories'].items():
        subcategories.append({
            'id': int(sub_id),
            'name': sub_data['name'],
            'itemCount': len(sub_data['products'])
        })
    
    time.sleep(0.4)  # Simulate network delay
    
    return jsonify({
        'categoryId': category_id,
        'categoryName': category['name'],
        'subcategories': subcategories,
        'timestamp': datetime.now().isoformat()
    })
```
**Purpose:** Get category with subcategories  
**URL:** `GET /categories/:id`  
**Auth:** Required  
**Delay:** 400ms  

---

#### **3. Products Endpoint (Lines 275-310)**
```python
@app.route('/categories/<int:category_id>/subcategories/<int:subcategory_id>', 
           methods=['GET'])
def get_subcategory_products(category_id, subcategory_id):
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    cat_key = str(category_id)
    sub_key = str(subcategory_id)
    
    if cat_key not in category_data or sub_key not in category_data[cat_key]['subcategories']:
        return jsonify({'error': 'Subcategory not found'}), 404
    
    subcategory = category_data[cat_key]['subcategories'][sub_key]
    
    time.sleep(0.5)  # Simulate network delay
    
    return jsonify({
        'categoryId': category_id,
        'subcategoryId': subcategory_id,
        'subcategoryName': subcategory['name'],
        'products': subcategory['products'],
        'totalProducts': len(subcategory['products']),
        'timestamp': datetime.now().isoformat()
    })
```
**Purpose:** Get all products in subcategory  
**URL:** `GET /categories/:id/subcategories/:id`  
**Auth:** Required  
**Delay:** 500ms  

---

### **Universal Route Handler (Lines 350-420)**
```python
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def universal_handler(path):
    request_path = '/' + path
    
    # Find matching endpoint
    matched_endpoint = None
    path_params = {}
    
    for endpoint in config['endpoints']:
        if endpoint['method'].upper() != request.method:
            continue
        
        matches, params = path_matches(endpoint['path'], request_path)
        if matches:
            matched_endpoint = endpoint
            path_params = params
            break
    
    if not matched_endpoint:
        return jsonify({'error': 'Endpoint not found'}), 404
    
    # Apply delay
    delay = matched_endpoint.get('delay', 0)
    if delay > 0:
        time.sleep(delay / 1000.0)
    
    # Build context
    body_data = {}
    if request.method in ['POST', 'PUT', 'PATCH']:
        body_data = request.get_json(silent=True) or {}
    
    context = {
        'query': dict(request.args),
        'params': path_params,
        'body': body_data
    }
    
    # Process template
    response_data = process_template(matched_endpoint['response'], context)
    
    return jsonify(response_data), matched_endpoint['status']
```
**Purpose:** Handle all config.json defined endpoints  
**Process:**
1. Match request path with config patterns
2. Extract path parameters
3. Apply configured delay
4. Process template variables
5. Return response

---

### **Config File Watcher (Lines 430-460)**
```python
class ConfigFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('config.json'):
            print('🔄 Config file changed, reloading...')
            time.sleep(0.1)
            load_config()
            print('✅ Configuration reloaded')

def start_config_watcher():
    try:
        event_handler = ConfigFileHandler()
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()
        print('🔄 Auto-reload: ENABLED')
    except Exception as e:
        print(f'⚠️  Auto-reload: DISABLED ({str(e)})')
```
**Purpose:** Auto-reload config without restart  
**Library:** watchdog  
**Monitors:** config.json file  
**Action:** Reload config when file changes  

---

### **Main Function (Lines 470-510)**
```python
def main():
    import sys
    
    if not load_config():
        print('Failed to start server')
        exit(1)
    
    # Get port from command line, env, or config
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else \
           int(os.environ.get('PORT', config.get('port', 5600)))
    
    print(f'🚀 HTTP Stub Server running on http://localhost:{PORT}')
    print(f'📝 Logs: {LOG_PATH}')
    print(f'⚙️  Config: {CONFIG_PATH}')
    
    print('\n📋 Available endpoints:')
    if 'endpoints' in config:
        for ep in config['endpoints']:
            delay_info = f"[delay: {ep['delay']}ms]" if ep.get('delay') else ''
            print(f"   {ep['method']} {ep['path']} ({ep['status']}) {delay_info}")
    
    # Start config watcher
    watcher_thread = Thread(target=start_config_watcher, daemon=True)
    watcher_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    main()
```
**Purpose:** Server startup  
**Process:**
1. Load configuration
2. Get port (command line > env > config > default)
3. Display server info
4. Start config watcher
5. Start Flask server

---

## 📦 **2. data.py - Product Catalog**

### **Structure**
```python
category_data = {
    "1": {  # Electronics
        "name": "Electronics",
        "subcategories": {
            "1": {  # Laptops
                "name": "Laptops",
                "products": [
                    {
                        "id": 1001,
                        "name": "Dell Inspiron 15",
                        "price": 45000,
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "Intel i5, 8GB RAM, 512GB SSD"
                    },
                    # ... more products
                ]
            },
            # ... more subcategories
        }
    },
    # ... more categories
}
```

**Categories (6):**
1. Electronics
2. Clothing
3. TV & Appliances
4. Smartphones
5. Kitchen
6. Home Decor

**Subcategories (18):**
- 3 per category
- Example: Electronics → Laptops, Headphones, Cameras

**Products (60+):**
- 3-4 per subcategory
- Each has: id, name, price, rating, stock, specs

---

## ⚙️ **3. config.json - API Configuration**

### **Structure**
```json
{
  "port": 5600,
  "endpoints": [
    {
      "path": "/register",
      "method": "POST",
      "status": 200,
      "delay": 0,
      "response": {
        "success": true,
        "message": "User registered successfully",
        "userId": "{{randomId}}",
        "token": "{{randomId}}",
        "timestamp": "{{timestamp}}"
      }
    },
    // ... 14 more endpoints
  ]
}
```

**Endpoints (15+):**
1. POST /register
2. POST /login
3. GET /categories
4. GET /categories/:id
5. GET /categories/:id/subcategories/:id
6. GET /categories/:id/subcategories/:id/products/:id
7. POST /cart/add
8. GET /cart
9. POST /order/place
10. GET /orders
11. GET /order/:id
12. GET /search
13. GET /profile
14. POST /logout
15. GET /health

---

## 🎯 **Key Concepts for Viva**

### **1. Flask Framework**
**Q: What is Flask?**  
A: Flask is a lightweight Python web framework for building APIs and web applications.

**Q: Why Flask over Django?**  
A: Flask is simpler, more flexible, and perfect for API-only projects. Django is heavier with built-in features we don't need.

---

### **2. RESTful API**
**Q: What is REST?**  
A: REST (Representational State Transfer) is an architectural style for APIs using HTTP methods.

**HTTP Methods:**
- GET: Retrieve data
- POST: Create data
- PUT: Update data
- DELETE: Remove data

---

### **3. Authentication**
**Q: How does authentication work?**  
A: 
1. User registers/logs in
2. Server generates token
3. Client stores token
4. Client sends token in Authorization header
5. Server validates token for protected routes

---

### **4. CORS**
**Q: What is CORS?**  
A: Cross-Origin Resource Sharing allows frontend (different domain) to access backend API.

**Q: Why needed?**  
A: Browsers block cross-origin requests by default for security. CORS enables it.

---

### **5. Template Variables**
**Q: What are template variables?**  
A: Placeholders in config.json that get replaced with dynamic values.

**Examples:**
- `{{timestamp}}` → Current time
- `{{randomId}}` → Unique ID
- `{{body.email}}` → Request body field

---

### **6. Hot Reload**
**Q: What is hot reload?**  
A: Automatically reload configuration when config.json changes, without restarting server.

**Q: How implemented?**  
A: Using watchdog library to monitor file changes.

---

### **7. PyPI Package**
**Q: What is PyPI?**  
A: Python Package Index - repository for Python packages.

**Q: How to install your package?**  
A: `pip install http-stub-server`

**Q: How to run?**  
A: `http-stub-server` (one command!)

---

## 📊 **Project Statistics**

- **Total Lines:** 900+
- **Functions:** 15+
- **Endpoints:** 15+
- **Products:** 60+
- **Categories:** 6
- **Subcategories:** 18
- **Dependencies:** 3 (Flask, Flask-CORS, watchdog)
- **Python Version:** 3.8+
- **Package Size:** ~70KB

---

## 🎓 **Common Viva Questions & Answers**

### **Q1: Explain your project in 2 minutes**
**A:** "I've built an HTTP Stub Server - a mock e-commerce API that simulates a real backend. It has 15+ endpoints for authentication, product browsing, cart, and orders. Built with Python Flask, it features token-based auth, dynamic routing from JSON config, template variables, request logging, and hot-reload. I've also published it on PyPI, so anyone can install it with `pip install http-stub-server`. It has 60+ products across 6 categories and is production-ready with complete documentation."

---

### **Q2: Why Python instead of Node.js?**
**A:** "Python is more readable and beginner-friendly. Flask is simpler than Express. Python's synchronous model is easier to understand than Node's async callbacks. Plus, Python has better data science integration if we want to add analytics later."

---

### **Q3: How does authentication work?**
**A:** "When user registers or logs in, server generates a random token using Python's secrets module. Client stores this token and sends it in Authorization header for protected routes. Server checks if token exists - if yes, allow access; if no, return 401 Unauthorized."

---

### **Q4: What is the purpose of template variables?**
**A:** "Template variables make responses dynamic. Instead of hardcoding values, we use placeholders like {{timestamp}} or {{randomId}} in config.json. When request comes, server replaces these with actual values - current time, random IDs, or data from request body/query params."

---

### **Q5: How does hot reload work?**
**A:** "I use watchdog library to monitor config.json file. When file changes, watchdog triggers an event. My handler catches this event and reloads configuration using json.load(). This way, I can add/modify endpoints without restarting server."

---

### **Q6: What is the advantage of PyPI package?**
**A:** "PyPI makes installation super easy - just `pip install http-stub-server`. No manual setup, no cloning repo, no dependency installation. It's professional, worldwide accessible, and shows industry-standard practices. Anyone can use it with one command."

---

### **Q7: How do you handle errors?**
**A:** "I use try-except blocks for file operations and JSON parsing. For API errors, I return proper HTTP status codes - 200 for success, 401 for unauthorized, 404 for not found, 500 for server errors. All errors are logged to file for debugging."

---

### **Q8: Explain the request flow**
**A:** 
1. Client sends HTTP request
2. Flask routes to appropriate handler
3. before_request middleware stores start time
4. Handler checks authentication if needed
5. Handler processes request (query params, body)
6. Template variables replaced with actual values
7. Configured delay applied (if any)
8. Response generated and sent
9. after_request middleware logs request
10. Client receives response

---

### **Q9: What are the main challenges you faced?**
**A:** 
1. Template variable replacement - solved using regex and string manipulation
2. Flask 3.0 GET request body issue - solved with conditional JSON parsing
3. Python 3.13 watchdog compatibility - added graceful error handling
4. Dynamic routing - solved with regex pattern matching

---

### **Q10: How would you scale this project?**
**A:** 
1. Add database (PostgreSQL/MongoDB) instead of in-memory data
2. Add Redis for caching
3. Implement JWT tokens instead of simple strings
4. Add rate limiting
5. Deploy on cloud (AWS/Azure)
6. Add Docker containerization
7. Implement CI/CD pipeline
8. Add monitoring (Prometheus/Grafana)

---

## ✅ **Final Tips for Viva**

1. **Be Confident:** You built this, you know it!
2. **Explain Simply:** Use simple words, avoid jargon
3. **Show Demo:** Live demo is impressive
4. **Mention PyPI:** This is your USP!
5. **Know Your Code:** Understand every function
6. **Be Honest:** If you don't know, say "I'll learn that"
7. **Highlight Features:** 60+ products, 15+ endpoints, PyPI package
8. **Show Logs:** Demonstrate request logging
9. **Explain Choices:** Why Python? Why Flask? Why this approach?
10. **Be Enthusiastic:** Show passion for your project!

---

**Good luck with your viva! You've got this!** 🎉🚀

# 🎯 server.py - Complete Code Groups Summary

## 📋 All Groups at a Glance

| Group | Lines | Description | Key Concept |
|-------|-------|-------------|-------------|
| 1 | 1-6 | File Header | Documentation |
| 2 | 8-18 | Required Imports | Dependencies |
| 3 | 20-22 | Import Data | Product catalog |
| 4 | 29-30 | Import Data | In-memory database |
| 5 | 32-36 | Flask Init | App creation |
| 6 | 38-40 | Config Paths | Constants |
| 7 | 42-43 | Create Logs Dir | File system |
| 8 | 45-46 | Global Config | State management |
| 9 | 51-58 | generate_random_id() | Helper function |
| 10 | 61-76 | load_config() | File I/O |
| 11 | 78-105 | log_request() | Logging |
| 12 | 108-152 | process_template() | Template engine |
| 13 | 155-178 | path_matches() | URL routing |
| 14 | 183-188 | before_request() | Middleware |
| 15 | 191-215 | after_request() | Middleware |
| 16 | 220-242 | check_auth() | Authentication |
| 17 | 247-272 | home() | Root endpoint |
| 18 | 277-320 | get_category() | Category route |
| 19 | 323-365 | get_subcategory_products() | Products route |
| 20 | 368-430 | get_product_details() | Product detail route |
| 21 | 456-520 | universal_handler() | Dynamic router |
| 22 | 527-538 | ConfigFileHandler | File watcher class |
| 23 | 541-555 | start_config_watcher() | Start watcher |
| 24 | 561-595 | main() | Server startup |
| 25 | 598-599 | Entry point | if __name__ check |

---

## 🎓 Detailed Group Explanations

### GROUP 1: File Header (Lines 1-6)
```python
# ============================================
# HTTP STUB SERVER - PYTHON VERSION
# ============================================
```
**Purpose:** Documentation header
**Viva Point:** Explains project purpose

---

### GROUP 2: Required Imports (Lines 8-18)
```python
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json, time, re
from datetime import datetime
import random, string, os
from threading import Thread
```
**Purpose:** Import all dependencies
**Viva Point:** Each library's role

---

### GROUP 3: Import Data (Lines 20-22)
```python
from data import category_data
```
**Purpose:** Load product catalog
**Viva Point:** In-memory database concept

---

### GROUP 5: Flask Init (Lines 32-36)
```python
app = Flask(__name__)
CORS(app)
```
**Purpose:** Create Flask app
**Viva Point:** CORS explanation

---

### GROUP 6: Config Paths (Lines 38-40)
```python
CONFIG_PATH = 'config.json'
LOG_PATH = 'logs/requests.log'
```
**Purpose:** Define file paths
**Viva Point:** Constants best practice

---

### GROUP 7: Create Logs Dir (Lines 42-43)
```python
os.makedirs('logs', exist_ok=True)
```
**Purpose:** Ensure logs folder exists
**Viva Point:** exist_ok parameter

---

### GROUP 8: Global Config (Lines 45-46)
```python
config = {}
```
**Purpose:** Initialize config storage
**Viva Point:** Global variable usage

---

### GROUP 9: generate_random_id() (Lines 51-58)
```python
def generate_random_id():
    return ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=9
    ))
```
**Purpose:** Generate unique IDs
**Viva Point:** Random ID generation logic
**Example:** `"x5m9k2p7a"`

---

### GROUP 10: load_config() (Lines 61-76)
```python
def load_config():
    global config
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return True
    except Exception as e:
        return False
```
**Purpose:** Load config.json
**Viva Point:** 
- global keyword
- with statement
- Error handling

---

### GROUP 11: log_request() (Lines 78-105)
```python
def log_request(method, url, query_params, status_code, duration_ms):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'url': url,
        'status': status_code,
        'duration': f'{duration_ms}ms'
    }
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
```
**Purpose:** Log API requests
**Viva Point:**
- Append mode
- ISO timestamp
- Structured logging

---

### GROUP 12: process_template() (Lines 108-152)
```python
def process_template(obj, context):
    json_str = json.dumps(obj)
    
    # Replace {{timestamp}}
    json_str = json_str.replace('{{timestamp}}', datetime.now().isoformat())
    
    # Replace {{randomId}}
    while '{{randomId}}' in json_str:
        json_str = json_str.replace('{{randomId}}', generate_random_id(), 1)
    
    # Replace {{query.field}}, {{body.field}}, {{params.field}}
    for key, value in context.get('query', {}).items():
        json_str = json_str.replace(f'{{{{query.{key}}}}}', str(value))
    
    return json.loads(json_str)
```
**Purpose:** Replace template variables
**Viva Point:**
- Template engine concept
- Variable substitution
- Context-aware responses

**Example:**
```
Template: {"userId": "{{randomId}}", "productId": "{{body.productId}}"}
Context: {"body": {"productId": "2013"}}
Result: {"userId": "x5m9k2p7a", "productId": "2013"}
```

---

### GROUP 13: path_matches() (Lines 155-178)
```python
def path_matches(endpoint_path, request_path):
    # Convert :param to regex
    pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', endpoint_path)
    pattern = f'^{pattern}$'
    
    match = re.match(pattern, request_path)
    if match:
        return True, match.groupdict()
    return False, {}
```
**Purpose:** Match dynamic URL patterns
**Viva Point:**
- Regex pattern matching
- Named groups
- Parameter extraction

**Example:**
```
Endpoint: "/order/:orderId"
Request: "/order/ORD123"
Result: (True, {"orderId": "ORD123"})
```

---

### GROUP 14: before_request() (Lines 183-188)
```python
@app.before_request
def before_request():
    request.start_time = time.time()
```
**Purpose:** Record request start time
**Viva Point:**
- Middleware pattern
- Decorator usage
- Request timing

---

### GROUP 15: after_request() (Lines 191-215)
```python
@app.after_request
def after_request(response):
    duration = int((time.time() - request.start_time) * 1000)
    log_request(request.method, request.path, 
                dict(request.args), response.status_code, duration)
    return response
```
**Purpose:** Log request after processing
**Viva Point:**
- Middleware execution order
- Duration calculation
- Must return response

---

### GROUP 16: check_auth() (Lines 220-242)
```python
def check_auth():
    token = request.headers.get('Authorization') or request.args.get('token')
    
    if not token:
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Please login first!'
        }), 401
    
    return None  # Success
```
**Purpose:** Verify authentication token
**Viva Point:**
- Token validation
- 401 status code
- Two token sources (header/query)

---

### GROUP 17: home() (Lines 247-272)
```python
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'HTTP Stub Server',
        'status': 'running',
        'endpoints': {...}
    })
```
**Purpose:** Root endpoint / welcome page
**Viva Point:**
- Route decorator
- API discoverability
- Self-documentation

---

### GROUP 18: get_category() (Lines 277-320)
```python
@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    category_key = str(category_id)
    if category_key not in category_data:
        return jsonify({'error': 'Not found'}), 404
    
    # Build response...
    time.sleep(0.4)  # Simulate delay
    return jsonify(response_data)
```
**Purpose:** Get category with subcategories
**Viva Point:**
- URL parameters
- Authentication check
- Simulated delay
- 404 handling

---

### GROUP 19: get_subcategory_products() (Lines 323-365)
```python
@app.route('/categories/<int:category_id>/subcategories/<int:subcategory_id>')
def get_subcategory_products(category_id, subcategory_id):
    # Similar to get_category
    # Returns product list
```
**Purpose:** Get products in subcategory
**Viva Point:** Nested URL parameters

---

### GROUP 20: get_product_details() (Lines 368-430)
```python
@app.route('/categories/<int:category_id>/subcategories/<int:subcategory_id>/products/<int:product_id>')
def get_product_details(category_id, subcategory_id, product_id):
    # Returns single product details
```
**Purpose:** Get single product
**Viva Point:** Deep URL nesting

---

### GROUP 21: universal_handler() (Lines 456-520)
```python
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def universal_handler(path):
    request_path = '/' + path
    
    # Find matching endpoint in config
    for endpoint in config['endpoints']:
        if endpoint['method'] != request.method:
            continue
        
        matches, params = path_matches(endpoint['path'], request_path)
        if matches:
            matched_endpoint = endpoint
            break
    
    if not matched_endpoint:
        return jsonify({'error': 'Not found'}), 404
    
    # Apply delay
    delay = matched_endpoint.get('delay', 0)
    if delay > 0:
        time.sleep(delay / 1000.0)
    
    # Get request body
    body_data = request.get_json(silent=True) or {}
    
    # Build context
    context = {
        'query': dict(request.args),
        'params': path_params,
        'body': body_data
    }
    
    # Process template
    response_data = process_template(matched_endpoint['response'], context)
    
    return jsonify(response_data), matched_endpoint['status']
```
**Purpose:** Configuration-driven dynamic router
**Viva Point:**
- Catch-all route
- Config-driven behavior
- Template processing
- Delay simulation

**This is the CORE of the project!**

---

### GROUP 22: ConfigFileHandler (Lines 527-538)
```python
class ConfigFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('config.json'):
            print('🔄 Reloading...')
            time.sleep(0.1)
            load_config()
```
**Purpose:** Detect config file changes
**Viva Point:**
- Observer pattern
- File system events
- Auto-reload

---

### GROUP 23: Configuration Management (Lines 520-525)
```python
# Note: Config changes require server restart for simplicity
```
**Purpose:** Simplified configuration management
**Viva Point:** Production-ready approach
- Background thread
- Observer pattern
- Graceful degradation

---

### GROUP 24: main() (Lines 561-595)
```python
def main():
    import sys
    
    if not load_config():
        exit(1)
    
    # Get port (CLI > ENV > Config > Default)
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else \
           int(os.environ.get('PORT', config.get('port', 5600)))
    
    print(f'🚀 Server running on http://localhost:{PORT}')
    
    # Start file watcher
    watcher_thread = Thread(target=start_config_watcher, daemon=True)
    watcher_thread.start()
    
    # Start Flask
    app.run(host='0.0.0.0', port=PORT, debug=False)
```
**Purpose:** Initialize and start server
**Viva Point:**
- Port priority order
- Daemon thread
- host='0.0.0.0' explanation

---

### GROUP 25: Entry Point (Lines 598-599)
```python
if __name__ == '__main__':
    main()
```
**Purpose:** Run only when executed directly
**Viva Point:**
- __name__ variable
- Import vs execute

---

## 🎯 Key Concepts by Group

### Configuration-Driven (Groups 10, 12, 21)
- Load config from JSON
- Process templates
- Dynamic routing

### Middleware Pattern (Groups 14, 15, 16)
- before_request
- after_request
- check_auth

### Helper Functions (Groups 9, 10, 11, 12, 13)
- Reusable utilities
- Single responsibility
- Clean code

### Route Handlers (Groups 17-21)
- Flask decorators
- URL parameters
- Response generation

### File Watching (Groups 22, 23)
- Observer pattern
- Background threads
- Auto-reload

---

## 📝 Viva Preparation Checklist

- [ ] Explain each group's purpose
- [ ] Walk through request lifecycle
- [ ] Describe template processing
- [ ] Explain middleware execution order
- [ ] Discuss configuration-driven design
- [ ] Compare with real production API
- [ ] Explain error handling strategy
- [ ] Discuss scalability considerations

---

**Practice explaining 2-3 groups at a time! Good luck! 🚀**

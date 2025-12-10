# 📚 server.py - Group-wise Code Explanation

## Table of Contents
1. [Group 1: Imports & Dependencies](#group-1-imports--dependencies)
2. [Group 2: Flask App Setup](#group-2-flask-app-setup)
3. [Group 3: Helper Functions](#group-3-helper-functions)
4. [Group 4: Middleware](#group-4-middleware)
5. [Group 5: Route Handlers](#group-5-route-handlers)
6. [Group 6: File Watcher](#group-6-file-watcher)
7. [Group 7: Main Function](#group-7-main-function)

---

## Group 1: Imports & Dependencies

### **Lines 1-18: Import Statements**

```python
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import time
import re
from datetime import datetime
import random
import string
import os
from threading import Thread
```

**Purpose:** Import all required libraries

**Explanation:**
- **Flask imports** - Web framework core functionality
- **flask_cors** - Enable cross-origin requests (frontend can call API)
- **json** - Parse and generate JSON data
- **time** - Measure request duration and add delays
- **re** - Regular expressions for URL pattern matching
- **datetime** - Generate timestamps for logs and responses
- **random, string** - Generate random IDs (user IDs, tokens, order IDs)
- **os** - File system operations (create folders, read env variables)
- **threading** - Run file watcher in background

**Viva Q&A:**
- **Q:** Why Flask and not Django?
- **A:** Flask is lightweight and perfect for APIs. Django is better for full web apps with admin panels.

---

### **Lines 19-20: Import Product Data**

```python
from data import category_data
```

**Purpose:** Import product catalog from data.py

**Explanation:**
- **category_data** - Dictionary with all products
- **In-memory database** - Fast access, no DB setup needed
- **Production alternative** - Would be MongoDB/PostgreSQL

---

## Group 2: Flask App Setup

### **Lines 29-32: Flask Initialization**

```python
app = Flask(__name__)
CORS(app)
```

**Purpose:** Create Flask application instance

**Explanation:**
- **Flask(__name__)** - Create app, __name__ helps Flask locate resources
- **CORS(app)** - Allow all origins to access API (development friendly)

**Viva Q&A:**
- **Q:** What is CORS and why needed?
- **A:** Browser security blocks cross-origin requests. CORS allows frontend (localhost:3000) to call backend (localhost:5600).

---

### **Lines 34-40: Configuration Variables**

```python
CONFIG_PATH = 'config.json'
LOG_PATH = 'logs/requests.log'

os.makedirs('logs', exist_ok=True)

config = {}
```

**Purpose:** Define file paths and initialize storage

**Explanation:**
- **Constants** - Centralized path management
- **os.makedirs** - Create logs folder if doesn't exist
- **exist_ok=True** - Don't error if folder already exists
- **config = {}** - Global dictionary to store loaded configuration

---

## Group 3: Helper Functions

### **Lines 42-50: generate_random_id()**

```python
def generate_random_id():
    """
    Generates a random unique ID for users, orders, etc.
    Returns a 9-character alphanumeric string
    Example: "a7b3c9d2e"
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
```

**Purpose:** Generate unique IDs for users, orders, tokens

**Explanation:**
- **random.choices()** - Pick random characters
- **string.ascii_lowercase** - 'abcdefghijklmnopqrstuvwxyz'
- **string.digits** - '0123456789'
- **k=9** - Generate 9 characters
- **''.join()** - Combine list into string

**Example Output:** `"x5m9k2p7a"`, `"b3n8q1r4z"`

**Viva Q&A:**
- **Q:** Why 9 characters?
- **A:** Balance between uniqueness and readability. 36^9 = 101 billion combinations.

---


### **Lines 52-68: load_config()**

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

**Purpose:** Load configuration from config.json file

**Explanation:**
- **global config** - Modify global variable (not local)
- **with open()** - Context manager, auto-closes file
- **encoding='utf-8'** - Support Unicode characters
- **json.load()** - Parse JSON file to Python dict
- **try-except** - Handle file not found or invalid JSON
- **Return True/False** - Indicate success/failure

**Viva Q&A:**
- **Q:** Why global keyword?
- **A:** Without it, Python creates local variable. Global modifies the module-level config.

---

### **Lines 70-92: log_request()**

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
    
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f'Log write error: {str(e)}')
    
    print(f"[{log_entry['timestamp']}] {method} {url} - {status_code} ({duration_ms}ms)")
```

**Purpose:** Log every API request to file and console

**Explanation:**
- **log_entry dict** - Structured log data
- **datetime.now().isoformat()** - ISO 8601 timestamp: "2025-12-05T15:30:45"
- **'a' mode** - Append to file (don't overwrite)
- **json.dumps()** - Convert dict to JSON string
- **+ '\n'** - Each log on new line
- **Console print** - Real-time monitoring

**Viva Q&A:**
- **Q:** Why log to both file and console?
- **A:** File for permanent record, console for real-time debugging.

---

### **Lines 94-152: process_template()**

```python
def process_template(obj, context):
    # Convert to JSON string for processing
    json_str = json.dumps(obj)
    
    # Replace timestamp
    json_str = json_str.replace('{{timestamp}}', datetime.now().isoformat())
    
    # Replace randomId (each occurrence gets unique ID)
    while '{{randomId}}' in json_str:
        json_str = json_str.replace('{{randomId}}', generate_random_id(), 1)
    
    # Replace query parameters
    for key, value in context.get('query', {}).items():
        placeholder = '{{query.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Replace body parameters
    for key, value in context.get('body', {}).items():
        placeholder = '{{body.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Replace path parameters
    for key, value in context.get('params', {}).items():
        placeholder = '{{params.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Convert back to object
    return json.loads(json_str)
```

**Purpose:** Replace template variables with actual values

**Explanation:**

**Step 1: Convert to String**
- Work with string for easy find-replace

**Step 2: Replace {{timestamp}}**
- Current time in ISO format

**Step 3: Replace {{randomId}}**
- While loop ensures each occurrence gets unique ID
- Replace only 1 at a time (third parameter)

**Step 4-6: Replace Context Variables**
- **{{query.token}}** → URL parameter value
- **{{body.productId}}** → POST body field
- **{{params.orderId}}** → URL path parameter

**Step 7: Convert Back**
- json.loads() converts string back to dict

**Example:**
```
Input Template:
{
  "userId": "{{randomId}}",
  "productId": "{{body.productId}}",
  "timestamp": "{{timestamp}}"
}

Context:
{
  "body": {"productId": "2013"}
}

Output:
{
  "userId": "x5m9k2p7a",
  "productId": "2013",
  "timestamp": "2025-12-05T15:30:45.123456"
}
```

**Viva Q&A:**
- **Q:** Why convert to string and back?
- **A:** String operations are simpler than recursive dict traversal. Performance is acceptable for API responses.

---

### **Lines 154-178: path_matches()**

```python
def path_matches(endpoint_path, request_path):
    # Convert :param syntax to regex
    pattern = endpoint_path
    pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
    pattern = f'^{pattern}$'
    
    # Try to match
    match = re.match(pattern, request_path)
    if match:
        return True, match.groupdict()
    return False, {}
```

**Purpose:** Match dynamic URL paths and extract parameters

**Explanation:**

**Step 1: Convert to Regex**
```
Input:  "/order/:orderId"
Regex:  r':(\w+)'  matches ":orderId"
Replace: r'(?P<\1>[^/]+)'  becomes "(?P<orderId>[^/]+)"
Result: "/order/(?P<orderId>[^/]+)"
```

**Step 2: Add Anchors**
- `^` - Start of string
- `$` - End of string
- Ensures exact match, not partial

**Step 3: Match and Extract**
- `re.match()` - Try to match pattern
- `groupdict()` - Extract named groups as dict

**Example:**
```
Endpoint: "/order/:orderId"
Request:  "/order/ORD123"

Pattern becomes: "^/order/(?P<orderId>[^/]+)$"
Match: True
Params: {"orderId": "ORD123"}
```

**Viva Q&A:**
- **Q:** What is (?P<name>...)?
- **A:** Named capturing group in regex. Captures value and assigns it a name.

---

## Group 4: Middleware

### **Lines 180-195: before_request()**

```python
@app.before_request
def before_request():
    """
    Executes before each request
    Stores request start time for performance logging
    """
    request.start_time = time.time()
```

**Purpose:** Record request start time

**Explanation:**
- **@app.before_request** - Flask decorator, runs before every request
- **request.start_time** - Add custom attribute to request object
- **time.time()** - Current time in seconds since epoch (1970-01-01)

**Viva Q&A:**
- **Q:** Can we add custom attributes to request?
- **A:** Yes! Flask's request object is flexible. We use it to pass data between middleware functions.

---

### **Lines 197-218: after_request()**

```python
@app.after_request
def after_request(response):
    """
    Executes after each request
    Logs request details to file for monitoring and debugging
    """
    # Calculate duration
    duration = int((time.time() - request.start_time) * 1000)
    
    # Log the request
    log_request(
        request.method,
        request.path,
        dict(request.args),
        response.status_code,
        duration
    )
    
    return response
```

**Purpose:** Log request after processing

**Explanation:**
- **@app.after_request** - Runs after request processed, before sending response
- **Calculate duration** - (end_time - start_time) * 1000 = milliseconds
- **request.method** - GET, POST, PUT, DELETE, etc.
- **request.path** - URL path like "/cart/add"
- **request.args** - Query parameters as ImmutableMultiDict
- **dict()** - Convert to regular dict
- **response.status_code** - 200, 404, 500, etc.
- **Must return response** - Modified or original

**Viva Q&A:**
- **Q:** Why multiply by 1000?
- **A:** time.time() returns seconds. We want milliseconds for better precision.

---

### **Lines 220-242: check_auth()**

```python
def check_auth():
    """
    Validates user authentication via token
    """
    # Check for token in header or query
    token = request.headers.get('Authorization') or request.args.get('token')
    
    if not token:
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Please create an account or login first to browse products!',
            'redirectTo': '/register',
            'timestamp': datetime.now().isoformat()
        }), 401
    
    return None  # Authentication successful
```

**Purpose:** Check if request has authentication token

**Explanation:**
- **Two token sources** - Header (standard) or query param (testing)
- **request.headers.get()** - Get Authorization header
- **or operator** - If header not found, try query param
- **if not token** - No token provided
- **Return error tuple** - (response, status_code)
- **401 Unauthorized** - Standard HTTP status for auth failure
- **Return None** - Means success, no error

**Viva Q&A:**
- **Q:** Why accept token in two places?
- **A:** Header is REST standard. Query param makes testing easier (can test in browser).

---

## Group 5: Route Handlers

### **Lines 245-272: home() - Root Endpoint**

```python
@app.route('/', methods=['GET'])
def home():
    """
    Root endpoint - displays server information
    """
    return jsonify({
        'message': 'HTTP Stub Server - Python Version',
        'status': 'running',
        'port': config.get('port', 5600),
        'version': '1.0.0',
        'endpoints': {
            'authentication': ['/register', '/login'],
            'categories': ['/categories', '/categories/:id'],
            'products': [...],
            'cart': ['/cart', '/cart/add'],
            'orders': ['/orders', '/order/place', '/order/:id'],
            'other': ['/search', '/profile']
        },
        'documentation': 'See README.md for complete API documentation',
        'test': 'Run python test_api.py to test all endpoints'
    })
```

**Purpose:** Welcome page showing server info

**Explanation:**
- **@app.route('/')** - Handle requests to root URL
- **methods=['GET']** - Only accept GET requests
- **jsonify()** - Convert dict to JSON response with proper headers
- **Server metadata** - Status, version, available endpoints
- **Self-documenting** - Lists all endpoints

**Viva Q&A:**
- **Q:** Why have a root endpoint?
- **A:** API discoverability. Developers can see what's available without reading docs.

---

### **Lines 275-320: get_category() - Category Details**

```python
@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Returns category details with its subcategories
    """
    # Check authentication
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    # Convert to string key
    category_key = str(category_id)
    
    # Validate category exists
    if category_key not in category_data:
        return jsonify({'error': 'Category not found'}), 404
    
    category = category_data[category_key]
    
    # Build subcategories list
    subcategories = []
    for sub_id, sub_data in category['subcategories'].items():
        subcategories.append({
            'id': int(sub_id),
            'name': sub_data['name'],
            'itemCount': len(sub_data['products'])
        })
    
    # Prepare response
    response_data = {
        'categoryId': category_id,
        'categoryName': category['name'],
        'subcategories': subcategories,
        'timestamp': datetime.now().isoformat()
    }
    
    # Simulate delay
    time.sleep(0.4)
    
    return jsonify(response_data)
```

**Purpose:** Get category with subcategories

**Explanation:**

**Step 1: Authentication**
- Call check_auth()
- If returns error, return it immediately

**Step 2: Type Conversion**
- URL param is int: `category_id = 2`
- Data keys are strings: `"2"`
- Convert for lookup

**Step 3: Validation**
- Check if category exists
- Return 404 if not found

**Step 4: Build Response**
- Extract category data
- Loop through subcategories
- Count products in each

**Step 5: Simulate Delay**
- time.sleep(0.4) = 400ms delay
- Mimics database query time

**Viva Q&A:**
- **Q:** Why simulate delay?
- **A:** Real APIs have latency. This helps frontend developers test loading states and spinners.

---

### **Lines 450-620: universal_handler() - Dynamic Router**

```python
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def universal_handler(path):
    """
    Dynamically handles all endpoints defined in config.json
    """
    # Prepend slash
    request_path = '/' + path
    
    # Verify config loaded
    if 'endpoints' not in config:
        return jsonify({'error': 'No endpoints configured'}), 404
    
    # Find matching endpoint
    matched_endpoint = None
    path_params = {}
    
    for endpoint in config['endpoints']:
        # Check method
        if endpoint['method'].upper() != request.method:
            continue
        
        # Check path
        matches, params = path_matches(endpoint['path'], request_path)
        if matches:
            matched_endpoint = endpoint
            path_params = params
            break
    
    # Return 404 if no match
    if not matched_endpoint:
        return jsonify({
            'error': 'Endpoint not found in current configuration',
            'path': request_path,
            'method': request.method
        }), 404
    
    # Apply delay
    delay = matched_endpoint.get('delay', 0)
    if delay > 0:
        time.sleep(delay / 1000.0)
    
    # Get request body
    body_data = {}
    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            body_data = request.get_json(silent=True) or {}
        except Exception as e:
            body_data = {}
    
    # Build context
    context = {
        'query': dict(request.args),
        'params': path_params,
        'body': body_data
    }
    
    # Process template
    response_data = process_template(matched_endpoint['response'], context)
    
    # Create response
    response = jsonify(response_data)
    
    # Add custom headers
    if 'headers' in matched_endpoint:
        for key, value in matched_endpoint['headers'].items():
            response.headers[key] = value
    
    # Return with status code
    return response, matched_endpoint['status']
```

**Purpose:** Configuration-driven request handler

**Explanation:**

**Step 1: Normalize Path**
- Flask gives path without leading slash
- Add it for config matching

**Step 2: Find Matching Endpoint**
- Loop through config endpoints
- Check HTTP method match
- Check path pattern match
- Break on first match

**Step 3: Handle Not Found**
- If no match, return 404
- Include helpful error message

**Step 4: Apply Delay**
- Get delay from config (default 0)
- Convert milliseconds to seconds
- Sleep to simulate latency

**Step 5: Extract Request Body**
- Only for POST/PUT/PATCH
- Use silent=True to avoid errors
- Default to empty dict if fails

**Step 6: Build Context**
- Collect all request data
- Query params, path params, body
- Pass to template processor

**Step 7: Process Template**
- Replace all {{variables}}
- Generate dynamic response

**Step 8: Add Custom Headers**
- If config specifies headers
- Add them to response

**Step 9: Return Response**
- With configured status code

**Viva Q&A:**
- **Q:** Why one handler for all endpoints?
- **A:** Configuration-driven design. Add endpoints without code changes. DRY principle.

- **Q:** What if two endpoints match?
- **A:** First match wins. Order in config.json matters.

---

## Group 6: File Watcher

### **Lines 525-530: Configuration Management**

**Note:** Configuration management has been simplified for production use. Config changes require server restart for stability and simplicity.

---

## Group 7: Main Function

### **Lines 580-620: main() - Server Startup**

```python
def main():
    """
    Main entry point for the HTTP Stub Server
    """
    import sys
    
    # Load configuration
    if not load_config():
        print('Failed to start server due to config error')
        exit(1)
    
    # Get port (priority: CLI > ENV > Config > Default)
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('PORT', config.get('port', 5600)))
    
    # Display startup info
    print(f'🚀 HTTP Stub Server running on http://localhost:{PORT}')
    print(f'📝 Logs are being written to: {LOG_PATH}')
    print(f'⚙️  Config file: {CONFIG_PATH}')
    
    # List endpoints
    print('\n📋 Available endpoints:')
    if 'endpoints' in config:
        for ep in config['endpoints']:
            delay_info = f"[delay: {ep['delay']}ms]" if ep.get('delay') else ''
            print(f"   {ep['method']} {ep['path']} ({ep['status']}) {delay_info}")
    
    # Start file watcher
    watcher_thread = Thread(target=start_config_watcher, daemon=True)
    watcher_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=PORT, debug=False)
```

**Purpose:** Initialize and start server

**Explanation:**

**Step 1: Load Config**
- Call load_config()
- Exit if fails (can't run without config)
- exit(1) = error code

**Step 2: Determine Port**
Priority order:
1. Command line: `python server.py 8080`
2. Environment: `PORT=8080`
3. Config file: `"port": 5600`
4. Default: `5600`

**Step 3: Display Info**
- Server URL
- Log file location
- Config file path
- List all endpoints

**Step 4: Start File Watcher**
- Create thread
- daemon=True = dies with main program
- Start in background

**Step 5: Start Flask**
- host='0.0.0.0' = accept external connections
- port=PORT = configured port
- debug=False = production mode

**Viva Q&A:**
- **Q:** Why host='0.0.0.0' not 'localhost'?
- **A:** 'localhost' only accepts local connections. '0.0.0.0' accepts from any IP (needed for deployment).

- **Q:** Why debug=False?
- **A:** Debug mode has auto-reload and detailed errors. Not needed in production, can be security risk.

---

### **Lines 622-624: Entry Point**

```python
if __name__ == '__main__':
    main()
```

**Purpose:** Run main() only when script is executed directly

**Explanation:**
- **__name__** - Special variable
- When run directly: `__name__ == '__main__'`
- When imported: `__name__ == 'server'`
- Prevents auto-run on import

**Viva Q&A:**
- **Q:** Why this check?
- **A:** Allows importing functions without starting server. Useful for testing.

---

## 🎯 Summary by Group

### **Group 1: Imports (Lines 1-20)**
- Import all required dependencies

### **Group 2: Setup (Lines 29-40)**
- Initialize Flask app
- Configure paths
- Create storage

### **Group 3: Helpers (Lines 42-178)**
- generate_random_id() - Create unique IDs
- load_config() - Read config file
- log_request() - Write logs
- process_template() - Replace variables
- path_matches() - Match URL patterns

### **Group 4: Middleware (Lines 180-242)**
- before_request() - Start timer
- after_request() - Log request
- check_auth() - Verify token

### **Group 5: Routes (Lines 245-620)**
- home() - Welcome page
- get_category() - Category details
- get_subcategory_products() - Product list
- get_product_details() - Single product
- universal_handler() - Config-driven router

### **Group 6: File Watcher (Lines 525-575)**
- ConfigFileHandler - Detect changes
- start_config_watcher() - Start monitoring

### **Group 7: Main (Lines 580-624)**
- main() - Initialize and start
- Entry point check

---

## 🎓 Key Concepts

### **1. Configuration-Driven Design**
- Behavior controlled by config.json
- No code changes for new endpoints
- Flexible and maintainable

### **2. Middleware Pattern**
- before_request, after_request
- Cross-cutting concerns (logging, timing)
- Reusable across all routes

### **3. Template Processing**
- Dynamic response generation
- Variable substitution
- Context-aware responses

### **4. Error Handling**
- Try-except blocks everywhere
- Graceful degradation
- Helpful error messages

### **5. Separation of Concerns**
- Each function has single responsibility
- Helper functions are reusable
- Clean code structure

---

## 📝 Viva Preparation Tips

### **Be Ready to Explain:**
1. Why Flask over other frameworks
2. How template processing works
3. Middleware execution order
4. Configuration-driven architecture
5. Error handling strategy
6. Performance considerations
7. Security measures
8. Deployment process

### **Common Questions:**
- Walk through a request lifecycle
- Explain how dynamic routing works
- Describe the template system
- Discuss scalability
- Compare with real production API

---

**Practice explaining each group! Good luck! 🚀**

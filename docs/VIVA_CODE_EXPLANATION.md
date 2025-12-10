# 🎓 Complete Code Explanation - Viva Preparation

## 📋 Table of Contents
1. [server.py - Main Server](#1-serverpy---main-server)
2. [data.py - Product Data](#2-datapy---product-data)
3. [config.json - Configuration](#3-configjson---configuration)
4. [setup.py - Package Setup](#4-setuppy---package-setup)
5. [requirements.txt - Dependencies](#5-requirementstxt---dependencies)

---

## 1. server.py - Main Server

### **Line 1-14: Import Statements**

```python
from flask import Flask, request, jsonify, Response
```
**Q: Flask kya hai?**
**A:** Flask ek lightweight Python web framework hai jo web applications aur APIs banane ke liye use hota hai.

**Q: request, jsonify, Response kya hain?**
**A:** 
- `request` - Client se aane wali HTTP request ko access karne ke liye
- `jsonify` - Python dictionary ko JSON response mein convert karne ke liye
- `Response` - Custom HTTP response banane ke liye

```python
from flask_cors import CORS
```
**Q: CORS kya hai aur kyun chahiye?**
**A:** CORS (Cross-Origin Resource Sharing) browser security feature hai. Ye allow karta hai ki different domain se API call ho sake. Frontend (localhost:3000) se backend (localhost:5600) call karne ke liye zaruri hai.

```python
import json
```
**Q: json module kya karta hai?**
**A:** JSON data ko read/write karne ke liye. Config file load karne aur responses generate karne mein use hota hai.

```python
import time
```
**Q: time module kyun import kiya?**
**A:** 
1. Request processing time calculate karne ke liye
2. Artificial delay add karne ke liye (network latency simulation)

```python
import re
```
**Q: re module kya hai?**
**A:** Regular expressions ke liye. Dynamic URL paths match karne mein use hota hai (e.g., `/order/:orderId`)

```python
from datetime import datetime
```
**Q: datetime kyun chahiye?**
**A:** Timestamps generate karne ke liye - logs mein aur API responses mein.

```python
import random
import string
```
**Q: Ye dono kyun import kiye?**
**A:** Random IDs generate karne ke liye (user IDs, order IDs, tokens, etc.)

```python
import os
```
**Q: os module ka use?**
**A:** 
1. File paths manage karne ke liye
2. Directories create karne ke liye (logs folder)
3. Environment variables read karne ke liye (PORT)

```python
from threading import Thread
```
**Q: Threading kyun use ki?**
**A:** Config file watcher ko background mein run karne ke liye, taaki main server block na ho.

**Note:** Project ab sirf essential dependencies use karta hai production stability ke liye.

```python
from data import category_data
```
**Q: Ye kya import kar rahe ho?**
**A:** `data.py` file se product catalog import kar rahe hain. Ye in-memory database ki tarah kaam karta hai.

---

### **Line 20-25: Flask App Initialization**

```python
app = Flask(__name__)
```
**Q: Ye line kya karti hai?**
**A:** Flask application instance create karti hai. `__name__` current module ka naam hai.

```python
CORS(app)
```
**Q: CORS enable karne se kya hota hai?**
**A:** Saare domains se API access allow ho jata hai. Development mein useful hai.

---

### **Line 27-30: Configuration**

```python
CONFIG_PATH = 'config.json'
LOG_PATH = 'logs/requests.log'
```
**Q: Constants kyun banaye?**
**A:** File paths ko ek jagah define karne se code maintainable rehta hai. Agar path change karna ho toh ek jagah change karo.

```python
os.makedirs('logs', exist_ok=True)
```
**Q: exist_ok=True ka matlab?**
**A:** Agar folder already exist karta hai toh error nahi throw karega. Safe way hai directory create karne ka.

```python
config = {}
```
**Q: Empty dictionary kyun banai?**
**A:** Global variable hai jo config.json ka data store karega. Saare functions access kar sakte hain.

---

### **Line 38-50: Helper Function - generate_random_id()**

```python
def generate_random_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
```
**Q: Ye function kya karta hai?**
**A:** 9 character ka random alphanumeric ID generate karta hai.

**Q: random.choices kya hai?**
**A:** Random selection karta hai given characters se.

**Q: string.ascii_lowercase + string.digits kya hai?**
**A:** 'abcdefghijklmnopqrstuvwxyz0123456789' - lowercase letters aur digits.

**Q: k=9 ka matlab?**
**A:** 9 characters select karo.

**Example Output:** `"a7b3c9d2e"`, `"x5y8z1m4n"`

---

### **Line 52-65: Helper Function - load_config()**

```python
def load_config():
    global config
```
**Q: global keyword kyun use kiya?**
**A:** Function ke andar global variable modify karne ke liye. Bina global ke, local variable ban jata.

```python
try:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
```
**Q: with statement ka use?**
**A:** File automatically close ho jati hai, chahe error aaye ya na aaye. Resource management ke liye best practice.

**Q: encoding='utf-8' kyun?**
**A:** Unicode characters (Hindi, emojis, special symbols) properly read ho sakein.

**Q: json.load() kya karta hai?**
**A:** JSON file ko Python dictionary mein convert karta hai.

```python
except Exception as e:
    print(f'❌ Error loading config: {str(e)}')
    return False
```
**Q: Exception handling kyun ki?**
**A:** Agar file nahi mili ya invalid JSON hai toh server crash na ho, gracefully handle ho.

---

### **Line 67-90: Helper Function - log_request()**

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
```
**Q: isoformat() kya hai?**
**A:** ISO 8601 format mein timestamp return karta hai: `"2025-12-05T15:30:45.123456"`

**Q: f-string kya hai?**
**A:** Python 3.6+ ka feature. Variables ko string mein embed karne ke liye: `f'{duration_ms}ms'`

```python
try:
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')
```
**Q: 'a' mode ka matlab?**
**A:** Append mode - file ke end mein add karta hai, overwrite nahi karta.

**Q: json.dumps() kya hai?**
**A:** Python dictionary ko JSON string mein convert karta hai.

---

### **Line 92-150: Helper Function - process_template()**

```python
def process_template(obj, context):
    json_str = json.dumps(obj)
```
**Q: Object ko string mein kyun convert kiya?**
**A:** String mein find-replace karna easy hai. Template variables replace karne ke liye.

```python
json_str = json_str.replace('{{timestamp}}', datetime.now().isoformat())
```
**Q: Template variable kya hai?**
**A:** Placeholder hai jo runtime pe actual value se replace hota hai.

**Example:**
```
Input:  "createdAt": "{{timestamp}}"
Output: "createdAt": "2025-12-05T15:30:45.123456"
```

```python
while '{{randomId}}' in json_str:
    json_str = json_str.replace('{{randomId}}', generate_random_id(), 1)
```
**Q: While loop kyun use ki?**
**A:** Multiple `{{randomId}}` ho sakte hain. Har ek ko unique ID chahiye.

**Q: replace() mein 1 ka matlab?**
**A:** Sirf pehli occurrence replace karo. Isse har randomId unique hoga.

```python
for key, value in context.get('query', {}).items():
    placeholder = '{{query.' + key + '}}'
    json_str = json_str.replace(placeholder, str(value))
```
**Q: context.get('query', {}) kya hai?**
**A:** Safely query parameters access karta hai. Agar nahi hai toh empty dict return karega.

**Q: str(value) kyun?**
**A:** Value koi bhi type ho sakti hai (int, bool). String mein convert karna zaruri hai.

**Example:**
```
URL: /search?q=laptop
Template: "searchTerm": "{{query.q}}"
Output: "searchTerm": "laptop"
```

```python
return json.loads(json_str)
```
**Q: json.loads() kya karta hai?**
**A:** JSON string ko wapas Python object mein convert karta hai.

---

### **Line 152-175: Helper Function - path_matches()**

```python
def path_matches(endpoint_path, request_path):
    pattern = endpoint_path
    pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
```
**Q: Regular expression kya kar raha hai?**
**A:** `:param` syntax ko regex named group mein convert kar raha hai.

**Example:**
```
Input:  "/order/:orderId"
Output: "/order/(?P<orderId>[^/]+)"
```

**Q: (?P<name>...) kya hai?**
**A:** Named capturing group. Match ko name se access kar sakte ho.

**Q: [^/]+ ka matlab?**
**A:** Slash ke alawa koi bhi character, ek ya zyada baar.

```python
pattern = f'^{pattern}$'
match = re.match(pattern, request_path)
```
**Q: ^ aur $ ka matlab?**
**A:** 
- `^` - String ki start
- `$` - String ki end
- Isse exact match hota hai, partial nahi

```python
if match:
    return True, match.groupdict()
return False, {}
```
**Q: groupdict() kya return karta hai?**
**A:** Named groups ko dictionary mein return karta hai.

**Example:**
```
Pattern: /order/(?P<orderId>[^/]+)
Request: /order/ORD123
Result: {'orderId': 'ORD123'}
```

---

### **Line 180-195: Middleware - before_request()**

```python
@app.before_request
def before_request():
    request.start_time = time.time()
```
**Q: @app.before_request decorator kya hai?**
**A:** Flask decorator hai jo har request se pehle execute hota hai.

**Q: request.start_time kya hai?**
**A:** Request object mein custom attribute add kar rahe hain. Duration calculate karne ke liye.

**Q: time.time() kya return karta hai?**
**A:** Current time in seconds since epoch (1 Jan 1970).

---

### **Line 197-215: Middleware - after_request()**

```python
@app.after_request
def after_request(response):
    duration = int((time.time() - request.start_time) * 1000)
```
**Q: @app.after_request kab execute hota hai?**
**A:** Response bhejne se pehle, har request ke baad.

**Q: Duration calculation kaise ho rahi hai?**
**A:** 
1. Current time - Start time = Seconds
2. Seconds * 1000 = Milliseconds
3. int() se decimal remove kar rahe hain

```python
log_request(
    request.method,
    request.path,
    dict(request.args),
    response.status_code,
    duration
)
```
**Q: request.args kya hai?**
**A:** URL query parameters. Example: `?token=abc&id=123`

**Q: dict() kyun use kiya?**
**A:** request.args ImmutableMultiDict hai. Normal dict mein convert kar rahe hain.

---

### **Line 220-240: Authentication Middleware - check_auth()**

```python
def check_auth():
    token = request.headers.get('Authorization') or request.args.get('token')
```
**Q: or operator kaise kaam kar raha hai?**
**A:** Pehle header check karta hai, agar nahi mila toh query parameter check karta hai.

**Q: Two ways se token kyun accept kar rahe ho?**
**A:** Flexibility ke liye. Header standard hai, query parameter testing ke liye easy hai.

```python
if not token:
    return jsonify({
        'success': False,
        'error': 'Unauthorized',
        'message': 'Please create an account or login first to browse products!',
        'redirectTo': '/register',
        'timestamp': datetime.now().isoformat()
    }), 401
```
**Q: 401 status code ka matlab?**
**A:** Unauthorized - Authentication required but not provided.

**Q: Tuple return kyun kar rahe ho?**
**A:** Flask mein (response, status_code) tuple return kar sakte ho.

```python
return None
```
**Q: None return karne ka matlab?**
**A:** Authentication successful. No error.

---

### **Line 245-270: Root Endpoint - home()**

```python
@app.route('/', methods=['GET'])
def home():
```
**Q: @app.route decorator kya karta hai?**
**A:** URL path ko function se bind karta hai. Jab `/` pe request aaye, ye function execute hoga.

**Q: methods=['GET'] ka matlab?**
**A:** Sirf GET requests accept karenge. POST/PUT/DELETE reject honge.

```python
return jsonify({
    'message': 'HTTP Stub Server - Python Version',
    'status': 'running',
    'port': config.get('port', 5600),
    'version': '1.0.0',
    'endpoints': {...}
})
```
**Q: jsonify() vs json.dumps() mein difference?**
**A:** 
- `jsonify()` - Flask function, proper HTTP response banata hai with headers
- `json.dumps()` - Sirf string return karta hai

---

### **Line 275-320: Dynamic Category Routes**

```python
@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
```
**Q: <int:category_id> kya hai?**
**A:** URL parameter hai jo integer type ka hoga. Flask automatically convert kar deta hai.

**Example:** `/categories/2` → `category_id = 2` (integer)

```python
auth_error = check_auth()
if auth_error:
    return auth_error
```
**Q: Ye pattern kyun use kiya?**
**A:** Reusable authentication check. Har protected route mein same code repeat nahi karna padta.

```python
category_key = str(category_id)
if category_key not in category_data:
    return jsonify({'error': 'Category not found'}), 404
```
**Q: String mein kyun convert kiya?**
**A:** `category_data` dictionary mein keys strings hain: `"1"`, `"2"`, etc.

**Q: 404 status code ka matlab?**
**A:** Not Found - Requested resource doesn't exist.

```python
time.sleep(0.4)
```
**Q: Artificial delay kyun add ki?**
**A:** Real API behavior simulate karne ke liye. Network latency aur database query time.

---

### **Line 450-520: Universal Handler**

```python
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def universal_handler(path):
```
**Q: <path:path> kya hai?**
**A:** Catch-all route. Koi bhi URL match ho jayega.

**Q: Saare HTTP methods kyun allow kiye?**
**A:** Configuration-driven hai. Config file decide karegi kaun sa method valid hai.

```python
request_path = '/' + path
```
**Q: Slash kyun add kiya?**
**A:** Flask path mein leading slash nahi deta. Config mein paths `/cart/add` format mein hain.

```python
for endpoint in config['endpoints']:
    if endpoint['method'].upper() != request.method:
        continue
```
**Q: upper() kyun use kiya?**
**A:** Case-insensitive comparison. Config mein "POST" ho ya "post", dono kaam karenge.

**Q: continue statement kya karti hai?**
**A:** Current iteration skip karke next iteration pe jati hai.

```python
matches, params = path_matches(endpoint['path'], request_path)
if matches:
    matched_endpoint = endpoint
    path_params = params
    break
```
**Q: break statement kyun?**
**A:** Pehla match mil gaya toh loop stop karo. Efficiency ke liye.

```python
if not matched_endpoint:
    return jsonify({
        'error': 'Endpoint not found in current configuration',
        'path': request_path,
        'method': request.method
    }), 404
```
**Q: Helpful error message kyun?**
**A:** Debugging easy ho. Developer ko pata chal jaye ki kya galat hai.

```python
delay = matched_endpoint.get('delay', 0)
if delay > 0:
    time.sleep(delay / 1000.0)
```
**Q: 1000.0 se kyun divide kiya?**
**A:** Config mein delay milliseconds mein hai. time.sleep() seconds leta hai.

**Q: .0 kyun lagaya?**
**A:** Float division ensure karne ke liye. Python 2 compatibility (though not needed in Python 3).

```python
body_data = {}
if request.method in ['POST', 'PUT', 'PATCH']:
    try:
        body_data = request.get_json(silent=True) or {}
    except Exception as e:
        body_data = {}
```
**Q: silent=True ka matlab?**
**A:** Agar JSON parse fail ho toh exception throw nahi karega, None return karega.

**Q: or {} kyun?**
**A:** Agar None return ho toh empty dict use karo.

**Q: Try-except kyun?**
**A:** Extra safety. Koi bhi unexpected error handle ho jaye.

```python
context = {
    'query': dict(request.args),
    'params': path_params,
    'body': body_data
}
```
**Q: Context object ka purpose?**
**A:** Template processing ke liye saara data ek jagah collect kar rahe hain.

```python
response_data = process_template(matched_endpoint['response'], context)
```
**Q: Ye line kya kar rahi hai?**
**A:** Config se response template le rahe hain aur variables replace kar rahe hain.

```python
response = jsonify(response_data)

if 'headers' in matched_endpoint:
    for key, value in matched_endpoint['headers'].items():
        response.headers[key] = value
```
**Q: Custom headers kyun add kar rahe ho?**
**A:** Config mein custom headers define kar sakte hain (e.g., Cache-Control, Custom-Header).

```python
return response, matched_endpoint['status']
```
**Q: Status code config se kyun le rahe ho?**
**A:** Flexibility. Har endpoint ka apna status code ho sakta hai (200, 201, 404, etc.).

---

### **Line 525-550: Config File Watcher**

**Note:** Configuration management ab simple hai - config changes ke liye server restart karna padta hai production stability ke liye.

---

### **Line 555-590: Main Function**

```python
def main():
    import sys
```
**Q: Function ke andar import kyun?**
**A:** Lazy import. Sirf jab main() call ho tab import ho. Module level import se conflict avoid karne ke liye.

```python
if not load_config():
    print('Failed to start server due to config error')
    exit(1)
```
**Q: exit(1) ka matlab?**
**A:** Program terminate karo with error code 1. OS ko pata chal jaye ki error hui.

```python
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('PORT', config.get('port', 5600)))
```
**Q: Ye complex line kya kar rahi hai?**
**A:** Port priority order:
1. Command line argument: `python server.py 8080`
2. Environment variable: `PORT=8080`
3. Config file: `config.json` mein port
4. Default: `5600`

**Q: sys.argv kya hai?**
**A:** Command line arguments ka list. `sys.argv[0]` = script name, `sys.argv[1]` = first argument.

```python
watcher_thread = Thread(target=start_config_watcher, daemon=True)
watcher_thread.start()
```
**Q: daemon=True ka matlab?**
**A:** Daemon thread hai. Main program exit hone pe automatically terminate ho jayega.

**Q: Thread kyun use kiya?**
**A:** File watcher background mein chale, main server block na ho.

```python
app.run(host='0.0.0.0', port=PORT, debug=False)
```
**Q: host='0.0.0.0' ka matlab?**
**A:** Saare network interfaces pe listen karo. External access allow ho (not just localhost).

**Q: debug=False kyun?**
**A:** Production mode. Debug mode mein auto-reload aur detailed errors hote hain.

```python
if __name__ == '__main__':
    main()
```
**Q: Ye condition kyun check ki?**
**A:** Sirf jab script directly run ho tab main() call ho. Import karne pe nahi.

---

## 2. data.py - Product Data

```python
category_data = {
    "1": {
        "name": "Electronics",
        "subcategories": {
            "1": {
                "name": "Laptops",
                "products": [...]
            }
        }
    }
}
```

**Q: Ye file ka purpose kya hai?**
**A:** In-memory database ki tarah kaam karta hai. Real production mein ye MongoDB/PostgreSQL hoga.

**Q: Nested dictionary structure kyun?**
**A:** Hierarchical data represent karne ke liye: Category → Subcategory → Products

**Q: String keys kyun use kiye ("1", "2")?**
**A:** URL parameters strings hote hain. Direct comparison easy ho jata hai.

**Q: Products list mein kya data hai?**
**A:** Product objects with fields: id, name, price, rating, specs, etc.

---

## 3. config.json - Configuration

```json
{
  "port": 5600,
  "endpoints": [
    {
      "path": "/register",
      "method": "POST",
      "status": 201,
      "delay": 1000,
      "response": {...}
    }
  ]
}
```

**Q: JSON format kyun use kiya?**
**A:** 
1. Human-readable hai
2. Easy to edit
3. Language-independent
4. Standard format for configuration

**Q: Endpoints array kyun?**
**A:** Multiple endpoints define karne ke liye. Har endpoint ek object hai.

**Q: Template variables kaise kaam karte hain?**
**A:** `{{body.field}}`, `{{timestamp}}` runtime pe replace hote hain actual values se.

---

## 4. setup.py - Package Setup

```python
from setuptools import setup, find_packages
```
**Q: setuptools kya hai?**
**A:** Python package distribution ke liye standard library.

**Q: find_packages() kya karta hai?**
**A:** Automatically saare Python packages dhundta hai project mein.

```python
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
```
**Q: README ko kyun read kar rahe ho?**
**A:** PyPI pe package description ke liye. Detailed documentation dikhane ke liye.

```python
setup(
    name="http-stub-server",
    version="1.0.1",
    author="Soumya Sagar",
    ...
)
```
**Q: setup() function ka purpose?**
**A:** Package metadata define karta hai. PyPI pe publish karne ke liye zaruri hai.

**Q: classifiers kya hain?**
**A:** Package ko categorize karte hain. Users ko search mein help karta hai.

```python
entry_points={
    "console_scripts": [
        "http-stub-server=server:main",
    ],
}
```
**Q: entry_points ka matlab?**
**A:** CLI command define karta hai. Install karne ke baad `http-stub-server` command terminal mein available hoga.

---

## 5. requirements.txt - Dependencies

```
Flask==3.0.0
Flask-CORS==4.0.0
```

**Q: requirements.txt ka purpose?**
**A:** Project dependencies list karta hai. `pip install -r requirements.txt` se saare packages install ho jate hain.

**Q: Version numbers kyun specify kiye?**
**A:** Reproducibility ke liye. Har environment mein same versions install honge.

**Q: == vs >= mein difference?**
**A:** 
- `==` - Exact version
- `>=` - Minimum version (newer versions bhi chalenge)

---

## 🎯 Common Viva Questions

### **Architecture Questions:**

**Q: Ye project ka architecture kya hai?**
**A:** Configuration-driven REST API architecture. Client → Flask Server → Config File → Template Processing → JSON Response

**Q: Stateless vs Stateful?**
**A:** Stateless hai. Har request independent hai. Server state maintain nahi karta (except in-memory config).

**Q: Scalability kaise achieve karoge?**
**A:** 
1. Load balancer add karo (Nginx)
2. Multiple server instances run karo
3. Database add karo (currently in-memory)
4. Caching layer add karo (Redis)

### **Design Pattern Questions:**

**Q: Kaun se design patterns use kiye?**
**A:** 
1. **Middleware Pattern** - before_request, after_request
2. **Template Method Pattern** - process_template()
3. **Strategy Pattern** - Universal handler with config-driven behavior
4. **Observer Pattern** - File watcher

**Q: Separation of Concerns kaise achieve kiya?**
**A:** 
1. Data layer - data.py
2. Configuration - config.json
3. Business logic - server.py
4. Routing - Flask decorators

### **Security Questions:**

**Q: Security measures kya hain?**
**A:** 
1. CORS enabled (controlled access)
2. Token-based authentication simulation
3. Input validation (JSON parsing with error handling)
4. Error messages don't expose sensitive info

**Q: Production mein kya improvements karoge?**
**A:** 
1. Real JWT authentication
2. Rate limiting
3. Input sanitization
4. HTTPS enforcement
5. SQL injection prevention (if using database)

### **Performance Questions:**

**Q: Performance optimization kaise karoge?**
**A:** 
1. Caching add karo (Redis)
2. Database indexing
3. Async processing (Celery)
4. CDN for static content
5. Database connection pooling

**Q: Bottlenecks kahan ho sakte hain?**
**A:** 
1. File I/O (config loading, logging)
2. Template processing (string operations)
3. No database (in-memory data limited)

---

## 🎓 Pro Tips for Viva:

1. **Confident raho** - Agar kuch nahi pata toh honestly bolo "Sir, ye part maine implement nahi kiya, but concept samajhta hun"

2. **Examples do** - Har concept ko real example se explain karo

3. **Trade-offs discuss karo** - "Maine ye approach isliye use kiya kyunki... but production mein ye better hoga..."

4. **Future improvements batao** - Shows you're thinking ahead

5. **Code walk-through practice karo** - Har function ko line-by-line explain kar sako

---

**All the best for your viva! 🎉**

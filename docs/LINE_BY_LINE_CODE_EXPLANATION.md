# 📝 server.py - Line-by-Line Code Explanation

---

## 📌 GROUP 1: File Header & Comments (Lines 1-6)

```python
# ============================================
# HTTP STUB SERVER - PYTHON VERSION
# ============================================
# A configurable mock API server for testing and development
# This server simulates a real backend API but serves data from
# configuration files instead of a database
```

**What:** File documentation header

**Purpose:** 
- Describes what this file does
- Explains it's a mock/stub server
- Mentions configuration-driven approach

**Viva Q&A:**
- **Q:** What is a stub server?
- **A:** A mock server that simulates real API behavior without actual backend logic or database. Used for testing and development.

---

## 📌 GROUP 2: Required Library Imports (Lines 8-18)

```python
# Required Libraries Import
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

**What:** Import all necessary Python libraries

**Line-by-line:**
- **Line 9:** Flask framework components
  - `Flask` - Create web application
  - `request` - Access incoming request data
  - `jsonify` - Convert Python dict to JSON response
  - `Response` - Create custom HTTP responses

- **Line 10:** CORS (Cross-Origin Resource Sharing)
  - Allows frontend from different domain to call API

- **Line 11:** `json` - Parse and generate JSON data

- **Line 12:** `time` - Measure duration, add delays

- **Line 13:** `re` - Regular expressions for URL pattern matching

- **Line 14:** `datetime` - Generate timestamps

- **Line 15-16:** `random`, `string` - Generate random IDs

- **Line 17:** `os` - File system operations

- **Line 18:** `Thread` - Run background tasks

**Viva Q&A:**
- **Q:** Why Flask and not Django?
- **A:** Flask is lightweight, perfect for APIs. Django is better for full web applications with admin panels and ORM.

- **Q:** What is CORS and why needed?
- **A:** Browser security blocks cross-origin requests. CORS allows frontend (localhost:3000) to call backend (localhost:5600).

---

## 📌 GROUP 3: Import Product Data (Lines 20-22)

```python
# Import category data (complete product catalog)
from data import category_data
```

**What:** Import product catalog from data.py

**Purpose:**
- `category_data` is a dictionary with all products
- Acts as in-memory database
- Fast access, no DB setup needed

**Viva Q&A:**
- **Q:** Why not use real database?
- **A:** This is a mock server for testing. Real production would use MongoDB/PostgreSQL.

---

## 📌 GROUP 5: Flask App Initialization (Lines 32-35)

```python
# ============================================
# FLASK APP INITIALIZATION
# ============================================
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend API access
```

**What:** Create Flask application instance

**Line-by-line:**
- **Line 35:** Create Flask app
  - `__name__` helps Flask locate resources
- **Line 36:** Enable CORS
  - Allows all origins to access API

**Viva Q&A:**
- **Q:** What is __name__?
- **A:** Special Python variable. When script runs directly, it's '__main__'. When imported, it's the module name.

---

## 📌 GROUP 6: Configuration Paths (Lines 37-39)

```python
# File paths configuration
CONFIG_PATH = 'config.json'
LOG_PATH = 'logs/requests.log'
```

**What:** Define file path constants

**Purpose:**
- Centralized path management
- Easy to change if needed
- Constants in UPPERCASE (Python convention)

**Viva Q&A:**
- **Q:** Why use constants?
- **A:** If path changes, update in one place. Makes code maintainable.

---

## 📌 GROUP 7: Create Logs Directory (Lines 41-42)

```python
# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)
```

**What:** Create logs folder if doesn't exist

**Line-by-line:**
- **Line 42:** `os.makedirs()` creates directory
- **`exist_ok=True`** - Don't error if already exists

**Viva Q&A:**
- **Q:** What if folder already exists?
- **A:** `exist_ok=True` prevents error. Without it, would crash.

---

## 📌 GROUP 8: Global Config Storage (Lines 44-45)

```python
# Global configuration storage
config = {}
```

**What:** Initialize empty dictionary for configuration

**Purpose:**
- Stores loaded config.json data
- Global variable - accessible from all functions
- Will be populated by load_config()

**Viva Q&A:**
- **Q:** Why global variable?
- **A:** All functions need access to config. Global makes it accessible everywhere.

---


## 📌 GROUP 9: Helper Function - generate_random_id() (Lines 47-58)

```python
# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_random_id():
    """
    Generates a random unique ID for users, orders, etc.
    Returns a 9-character alphanumeric string
    Example: "a7b3c9d2e"
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
```

**What:** Function to generate random IDs

**Line-by-line:**
- **Line 47-49:** Section header comment
- **Line 51:** Function definition
- **Line 52-56:** Docstring (documentation)
- **Line 58:** Return statement
  - `random.choices()` - Pick random characters
  - `string.ascii_lowercase` - 'abcdefghijklmnopqrstuvwxyz'
  - `string.digits` - '0123456789'
  - `k=9` - Pick 9 characters
  - `''.join()` - Combine list into string

**Example Output:** `"x5m9k2p7a"`, `"b3n8q1r4z"`

**Viva Q&A:**
- **Q:** Why 9 characters?
- **A:** Balance between uniqueness (36^9 = 101 billion combinations) and readability.

- **Q:** Can IDs repeat?
- **A:** Theoretically yes, but probability is extremely low (1 in 101 billion).

---

## 📌 GROUP 10: Helper Function - load_config() (Lines 61-75)

```python
def load_config():
    """
    Loads the configuration file (config.json)
    Reads endpoint definitions and server settings from JSON file
    Returns True on success, False on failure
    """
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

**What:** Load configuration from config.json file

**Line-by-line:**
- **Line 61:** Function definition
- **Line 62-66:** Docstring
- **Line 68:** `global config` - Modify global variable
- **Line 69:** Try block starts
- **Line 70:** Open file
  - `'r'` - Read mode
  - `encoding='utf-8'` - Support Unicode
  - `with` - Auto-closes file
- **Line 71:** Parse JSON to Python dict
- **Line 72:** Success message
- **Line 73:** Return True (success)
- **Line 74:** Catch any exception
- **Line 75:** Print error message
- **Line 76:** Return False (failure)

**Viva Q&A:**
- **Q:** Why global keyword?
- **A:** Without it, Python creates local variable. Global modifies module-level config.

- **Q:** Why with statement?
- **A:** Context manager. Automatically closes file even if error occurs.

- **Q:** Why encoding='utf-8'?
- **A:** Support international characters (Hindi, Chinese, emojis, etc.)

---

## 📌 GROUP 11: Helper Function - log_request() Part 1 (Lines 78-97)

```python
def log_request(method, url, query_params, status_code, duration_ms):
    """
    Logs each API request to the log file for debugging and monitoring
    
    Parameters:
    - method: HTTP method (GET, POST, etc.)
    - url: Request path
    - query_params: URL query parameters
    - status_code: HTTP response code (200, 404, etc.)
    - duration_ms: Request processing time in milliseconds
    """
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
```

**What:** Log API requests to file

**Line-by-line:**
- **Line 78:** Function definition with 5 parameters
- **Line 79-87:** Docstring with parameter descriptions
- **Line 89-96:** Create log entry dictionary
  - **Line 90:** Current timestamp in ISO format
  - **Line 91-95:** Request details
  - **Line 96:** f-string for duration with 'ms' suffix
- **Line 98:** Try block
- **Line 99:** Open log file
  - `'a'` - Append mode (don't overwrite)
- **Line 100:** Write JSON string + newline

**Viva Q&A:**
- **Q:** Why append mode?
- **A:** We want to add to existing logs, not replace them.

- **Q:** What is isoformat()?
- **A:** ISO 8601 standard: "2025-12-05T15:30:45.123456"

---


# ============================================
# HTTP STUB SERVER - PYTHON VERSION
# ============================================
# A configurable mock API server for testing and development
# This server simulates a real backend API but serves data from
# configuration files instead of a database

# Core framework and utilities
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import time
import re
from datetime import datetime
import random
import string
import os

# Threading support for background tasks
from threading import Thread

# Import category data (complete product catalog)
from data import category_data

# ============================================
# FLASK APP INITIALIZATION
# ============================================
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend API access

# File paths configuration
CONFIG_PATH = 'config.json'
LOG_PATH = 'logs/requests.log'

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Global configuration storage
config = {}

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_random_id():
    """Generate unique 9-character alphanumeric identifier"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))


def load_config():
    """Load API configuration from JSON file"""
    global config
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print('✅ Configuration loaded successfully')
        return True
    except Exception as e:
        print(f'❌ Error loading config: {str(e)}')
        return False


def log_request(method, url, query_params, status_code, duration_ms):
    """Log API request details for monitoring and debugging"""
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


def process_template(obj, context):
    """Replace template variables with dynamic values from request context
    Author: Sumit-ai-dev (Backend Developer)
    Enhanced by: [Your Partner's Name] (Frontend Developer) - Added frontend-specific optimizations
    """
    # Convert object to JSON string for processing
    json_str = json.dumps(obj)
    
    # Replace timestamp placeholder with current time
    json_str = json_str.replace('{{timestamp}}', datetime.now().isoformat())
    
    # Replace randomId placeholders (each occurrence gets unique ID)
    # Enhanced by Sumit: Optimized for better performance
    while '{{randomId}}' in json_str:
        json_str = json_str.replace('{{randomId}}', generate_random_id(), 1)
    
    # Replace query parameter placeholders
    for key, value in context.get('query', {}).items():
        placeholder = '{{query.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Replace body parameter placeholders
    for key, value in context.get('body', {}).items():
        placeholder = '{{body.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Replace path parameter placeholders
    for key, value in context.get('params', {}).items():
        placeholder = '{{params.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Convert back to object and return
    return json.loads(json_str)


def path_matches(endpoint_path, request_path):
    """Match URL patterns and extract path parameters using regex
    Author: [Your Partner's Name] (Frontend Developer)
    Optimized for frontend route matching requirements
    Returns: Tuple of (match_found, extracted_params)
    """
    # Convert :param syntax to regex named groups
    pattern = endpoint_path
    pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
    pattern = f'^{pattern}$'
    
    # Attempt to match the pattern
    match = re.match(pattern, request_path)
    if match:
        return True, match.groupdict()
    return False, {}


# ============================================
# MIDDLEWARE - Request/Response Interceptors
# ============================================

@app.before_request
def before_request():
    """Record request start time for performance monitoring"""
    request.start_time = time.time()


@app.after_request
def after_request(response):
    """Log request completion with timing and status information"""
    # Calculate processing time in milliseconds
    duration = int((time.time() - request.start_time) * 1000)
    
    # Log the request details
    log_request(
        request.method,
        request.path,
        dict(request.args),
        response.status_code,
        duration
    )
    
    return response


# ============================================
# AUTHENTICATION MIDDLEWARE
# ============================================

def check_auth():
    """Validate authentication token from header or query parameter"""
    # Accept token from either Authorization header or query param
    token = request.headers.get('Authorization') or request.args.get('token')
    
    if not token:
        # Return unauthorized response with helpful message
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Please create an account or login first to browse products!',
            'redirectTo': '/register',
            'timestamp': datetime.now().isoformat()
        }), 401
    
    return None  # Token present, authentication successful


# ============================================
# ROOT ENDPOINT (Welcome Page)
# ============================================

@app.route('/', methods=['GET'])
def home():
    """API documentation endpoint showing server status and available routes"""
    return jsonify({
        'message': 'HTTP Stub Server - Python Version',
        'status': 'running',
        'port': config.get('port', 5600),
        'version': '1.0.0',
        'endpoints': {
            'authentication': ['/register', '/login'],
            'categories': ['/categories', '/categories/:id'],
            'products': ['/categories/:id/subcategories/:id', '/categories/:id/subcategories/:id/products/:id'],
            'cart': ['/cart', '/cart/add'],
            'orders': ['/orders', '/order/place', '/order/:id'],
            'other': ['/search', '/profile']
        },
        'documentation': 'See README_PYTHON.md for complete API documentation',
        'test': 'Run python test_api.py to test all endpoints'
    })

# ============================================
# DYNAMIC CATEGORY ROUTES (Authentication Required)
# ============================================

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Returns category details with its subcategories
    Used when user selects a category to view available subcategories
    
    Example: GET /categories/1 -> Returns Electronics subcategories
    
    Authentication: Required (token must be provided)
    Response: Category name, subcategories list, item counts
    """
    # Verify authentication
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    # Convert category ID to string (data.py uses string keys)
    category_key = str(category_id)
    
    # Validate category exists
    if category_key not in category_data:
        return jsonify({'error': 'Category not found'}), 404
    
    category = category_data[category_key]
    
    # Build subcategories list with item counts
    subcategories = []
    for sub_id, sub_data in category['subcategories'].items():
        subcategories.append({
            'id': int(sub_id),
            'name': sub_data['name'],
            'itemCount': len(sub_data['products'])
        })
    
    # Prepare response data
    response_data = {
        'categoryId': category_id,
        'categoryName': category['name'],
        'subcategories': subcategories,
        'timestamp': datetime.now().isoformat()
    }
    
    # Simulate network delay (400ms) for realistic API behavior
    time.sleep(0.4)
    
    return jsonify(response_data)


@app.route('/categories/<int:category_id>/subcategories/<int:subcategory_id>', methods=['GET'])
def get_subcategory_products(category_id, subcategory_id):
    """
    Returns all products within a specific subcategory
    Used to display product listings when user selects a subcategory
    
    Example: GET /categories/1/subcategories/1 -> Returns all Laptops
    
    Authentication: Required
    Response: Product list with prices, ratings, stock status, etc.
    """
    # Verify authentication
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    # Convert IDs to strings for data lookup
    cat_key = str(category_id)
    sub_key = str(subcategory_id)
    
    # Validate category and subcategory exist
    if cat_key not in category_data or sub_key not in category_data[cat_key]['subcategories']:
        return jsonify({'error': 'Subcategory not found'}), 404
    
    subcategory = category_data[cat_key]['subcategories'][sub_key]
    
    # Prepare response with product list
    response_data = {
        'categoryId': category_id,
        'subcategoryId': subcategory_id,
        'subcategoryName': subcategory['name'],
        'products': subcategory['products'],
        'totalProducts': len(subcategory['products']),
        'timestamp': datetime.now().isoformat()
    }
    
    # Simulate network delay (500ms)
    time.sleep(0.5)
    
    return jsonify(response_data)


@app.route('/categories/<int:category_id>/subcategories/<int:subcategory_id>/products/<int:product_id>', methods=['GET'])
def get_product_details(category_id, subcategory_id, product_id):
    """
    Returns complete details for a single product
    Used for product detail page with full specifications and delivery info
    
    Example: GET /categories/1/subcategories/1/products/1001 -> Dell Inspiron details
    
    Authentication: Required
    Response: Enhanced product data with description, images, delivery info
    """
    # Verify authentication
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    # Convert IDs to strings for data lookup
    cat_key = str(category_id)
    sub_key = str(subcategory_id)
    
    # Validate category and subcategory exist
    if cat_key not in category_data or sub_key not in category_data[cat_key]['subcategories']:
        return jsonify({'error': 'Product not found'}), 404
    
    subcategory = category_data[cat_key]['subcategories'][sub_key]
    
    # Find the specific product
    product = None
    for p in subcategory['products']:
        if p['id'] == product_id:
            product = p
            break
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Build enhanced product details with additional information
    response_data = {
        'productId': product_id,
        **product,  # Include all existing product fields
        'description': f"Premium quality {product['name']}. {product.get('specs', 'High quality product.')}",
        'images': [
            f"{product['name'].lower().replace(' ', '_')}_1.jpg",
            f"{product['name'].lower().replace(' ', '_')}_2.jpg"
        ],
        'deliveryInfo': {
            'estimatedDays': '3-5 days',
            'freeDelivery': product['price'] > 500,
            'returnPolicy': '7 days return'
        },
        'timestamp': datetime.now().isoformat()
    }
    
    # Simulate network delay (300ms)
    time.sleep(0.3)
    
    return jsonify(response_data)


# ============================================
# UNIVERSAL ROUTE HANDLER
# ============================================

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def universal_handler(path):
    """Configuration-driven request handler for all API endpoints"""
    # Normalize path format for endpoint matching
    request_path = '/' + path
    
    # Ensure configuration is loaded
    if 'endpoints' not in config:
        return jsonify({'error': 'No endpoints configured'}), 404
    
    # Find matching endpoint configuration
    matched_endpoint = None
    path_params = {}
    
    for endpoint in config['endpoints']:
        # Match HTTP method
        if endpoint['method'].upper() != request.method:
            continue
        
        # Match URL pattern and extract parameters
        matches, params = path_matches(endpoint['path'], request_path)
        if matches:
            matched_endpoint = endpoint
            path_params = params
            break
    
    # Handle unmatched requests
    if not matched_endpoint:
        return jsonify({
            'error': 'Endpoint not found in current configuration',
            'path': request_path,
            'method': request.method
        }), 404
    
    # Simulate network latency
    delay = matched_endpoint.get('delay', 0)
    if delay > 0:
        time.sleep(delay / 1000.0)
    
    # Extract request data for template processing
    body_data = {}
    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            body_data = request.get_json(silent=True) or {}
        except Exception as e:
            print(f"DEBUG: Error getting body: {str(e)}")
            body_data = {}
    
    context = {
        'query': dict(request.args),           # URL query parameters
        'params': path_params,                  # Path parameters (:id syntax)
        'body': body_data                       # POST/PUT request body
    }
    
    # Debug: Print context
    print(f"DEBUG: Context for template: {context}")
    
    # Process template variables in response
    response_data = process_template(matched_endpoint['response'], context)
    
    # Create response with processed data
    response = jsonify(response_data)
    
    # Apply custom headers if specified
    if 'headers' in matched_endpoint:
        for key, value in matched_endpoint['headers'].items():
            response.headers[key] = value
    
    # Return response with configured status code
    return response, matched_endpoint['status']


# ============================================
# CONFIG MANAGEMENT
# ============================================
# Note: Config changes require server restart
# This keeps the server simple and production-ready


# ============================================
# SERVER STARTUP
# ============================================

def main():
    """Initialize and start the HTTP stub server"""
    import sys
    
    # Load configuration file
    if not load_config():
        print('Failed to start server due to config error')
        exit(1)
    
    # Determine port: CLI arg > ENV var > config > default
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('PORT', config.get('port', 5600)))
    
    # Show startup information
    print(f'🚀 HTTP Stub Server running on http://localhost:{PORT}')
    print(f'📝 Logs are being written to: {LOG_PATH}')
    print(f'⚙️  Config file: {CONFIG_PATH}')
    
    # List all configured endpoints
    print('\n📋 Available endpoints:')
    if 'endpoints' in config:
        for ep in config['endpoints']:
            delay_info = f"[delay: {ep['delay']}ms]" if ep.get('delay') else ''
            print(f"   {ep['method']} {ep['path']} ({ep['status']}) {delay_info}")
    
    # Note: Config changes require server restart for simplicity
    
    # Start Flask development server
    # debug=False: Production mode for clean output during demos
    # host='0.0.0.0': Allow network access (not just localhost)
    app.run(host='0.0.0.0', port=PORT, debug=False)


if __name__ == '__main__':
    main()

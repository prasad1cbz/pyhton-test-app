#!/usr/bin/env python3
"""
Hello World Python Application
Enhanced web application with health checks, logging, and production features
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

@app.route('/')
def hello_world():
    """Main endpoint that returns a greeting message"""
    logger.info(f"Request received from {request.remote_addr}")
    return jsonify({
        'message': 'Hello, world!',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'environment': app.config['ENV']
    })

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'python-webapp'
    })

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'Python Web App',
        'version': '1.0.0',
        'description': 'Hello World Python Application',
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Main greeting endpoint'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check endpoint'},
            {'path': '/api/info', 'method': 'GET', 'description': 'API information'}
        ]
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.utcnow().isoformat()
    }), 500

@app.before_request
def log_request():
    """Log all incoming requests"""
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting Python Web App on {host}:{port}")
    logger.info(f"Environment: {app.config['ENV']}")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    app.run(host=host, port=port, debug=app.config['DEBUG']) 
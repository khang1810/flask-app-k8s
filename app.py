import os
import logging
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get configuration from environment variables
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
APP_NAME = os.getenv('APP_NAME', 'Flask-K8s-App')

@app.route('/')
def home():
    logger.info("Home endpoint accessed")
    return f"Hello from {APP_NAME} on Kubernetes 2!"

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes liveness probe"""
    logger.debug("Health check endpoint accessed")
    return jsonify({
        'status': 'healthy',
        'service': APP_NAME,
        'version': '1.0.0'
    }), 200

@app.route('/ready')
def ready():
    """Readiness check endpoint for Kubernetes readiness probe"""
    logger.debug("Readiness check endpoint accessed")
    return jsonify({
        'status': 'ready',
        'service': APP_NAME,
        'ready': True
    }), 200

@app.route('/info')
def info():
    """Application information endpoint"""
    logger.info("Info endpoint accessed")
    return jsonify({
        'app_name': APP_NAME,
        'host': HOST,
        'port': PORT,
        'environment': os.getenv('ENVIRONMENT', 'development')
    }), 200

if __name__ == '__main__':
    logger.info(f"Starting {APP_NAME} on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=False)

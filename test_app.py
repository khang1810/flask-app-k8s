import os
import sys
import unittest

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app module
from app import app


class FlaskAppTestCase(unittest.TestCase):
    """Test cases for the Flask application"""

    def setUp(self):
        """Set up test client before each test"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_endpoint(self):
        """Test the home endpoint returns correct message"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello from Flask-K8s-App on Kubernetes!', response.data)

    def test_health_endpoint(self):
        """Test the health endpoint returns correct JSON"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'Flask-K8s-App')
        self.assertEqual(data['version'], '1.0.0')

    def test_ready_endpoint(self):
        """Test the ready endpoint returns correct JSON"""
        response = self.app.get('/ready')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = response.get_json()
        self.assertEqual(data['status'], 'ready')
        self.assertEqual(data['service'], 'Flask-K8s-App')
        self.assertTrue(data['ready'])

    def test_info_endpoint(self):
        """Test the info endpoint returns correct JSON"""
        response = self.app.get('/info')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = response.get_json()
        self.assertEqual(data['app_name'], 'Flask-K8s-App')
        self.assertEqual(data['host'], '0.0.0.0')
        self.assertEqual(data['port'], 5000)
        self.assertEqual(data['environment'], 'development')

    def test_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404"""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
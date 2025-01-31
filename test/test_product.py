import unittest
from unittest.mock import patch
from app import app

class TestProductEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.models.Product.query.all')
    def test_get_products(self, mock_query_all):
        mock_query_all.return_value = [MockProduct(1, 'Widget', 10.99)]
        response = self.app.get('/api/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Widget', response.data.decode())

    def test_create_product(self):
        response = self.app.post('/api/products', json={'name': 'Widget', 'price': 10.99})
        self.assertEqual(response.status_code, 201)

    def test_update_product(self):
        response = self.app.put('/api/products/1', json={'name': 'Widget', 'price': 12.99})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
from app import app

class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.models.Order.query.all')
    def test_get_orders(self, mock_query_all):
        mock_query_all.return_value = [MockOrder(1, '2024-08-01', 'Completed')]
        response = self.app.get('/api/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Completed', response.data.decode())

    def test_create_order(self):
        response = self.app.post('/api/orders', json={'date': '2024-08-01', 'status': 'Pending'})
        self.assertEqual(response.status_code, 201)

    def test_update_order(self):
        response = self.app.put('/api/orders/1', json={'status': 'Shipped'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

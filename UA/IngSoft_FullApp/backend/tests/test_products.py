import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestProductAPI(unittest.TestCase):
    def test_list_products(self):
        response = client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.json())

    def test_list_categories(self):
        response = client.get("/categories")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

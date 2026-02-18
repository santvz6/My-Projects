import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.state import result_store

client = TestClient(app)

class TestWebhookAPI(unittest.TestCase):

    def test_receive_task_result_success(self):
        task_id = "abc123"
        payload = {
            "task_id": task_id,
            "state": "success",
            "predictions": [
                {"label": "shoes", "score": 0.85}
            ]
        }

        response = client.post("/webhook/task_completed", json=payload)
        self.assertEqual(response.status_code, 202)
        self.assertIn(task_id, result_store)
        self.assertNotEqual(result_store[task_id], "failed")

    def test_receive_task_result_failed(self):
        task_id = "abc124"
        payload = {
            "task_id": task_id,
            "state": "failed",
            "predictions": []
        }

        response = client.post("/webhook/task_completed", json=payload)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(result_store[task_id], "failed")

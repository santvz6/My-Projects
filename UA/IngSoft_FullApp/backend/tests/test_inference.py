import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.state import result_store

client = TestClient(app)

class TestInferenceAPI(unittest.TestCase):
    pass
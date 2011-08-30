import unittest
from django.test.client import Client

class SimpleTest(unittest.TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_latest(self):
        client = Client()
        response = client.get('/latest')
        self.failUnlessEqual(response.status_code, 200)

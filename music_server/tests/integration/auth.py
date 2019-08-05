from http import HTTPStatus
import os
os.environ['FLASK_ENV'] = 'testing'
import unittest
from unittest.mock import patch
from uuid import UUID

from db import get_database
from db.migrations.migrate import main as migrate
import generate_token
from main import create_app


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.db = get_database()
        for i in range(1, 2):
            migrate('testing', 'up', f'db.migrations.v{i}')

    def tearDown(self):
        for i in reversed(range(1, 2)):
            migrate('testing', 'down', f'db.migrations.v{i}')
    
    def test_authentication_fails_and_not_throws_with_missing_header(self):
        res = self.client.get('/')
        self.assertEqual(res._status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(res.json['error'], 'Invalid token')
    
    def test_authentication_fails_and_not_throws_with_invalid_token(self):
        res = self.client.get('/', headers={'Authorization': 'Bearer invalid'})
        self.assertEqual(res._status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(res.json['error'], 'Invalid token')
    
    @patch('generate_token.uuid.uuid4')
    def test_authentication_works(self, mock):
        mock.return_value = UUID(int=42)
        generate_token.generate_token()
        res = self.client.get('/', headers={'Authorization': f'Bearer {"00000000-0000-0000-0000-00000000002a"}'})
        self.assertEqual(res._status_code, HTTPStatus.OK)
    

if __name__ == '__main__':
    unittest.main()

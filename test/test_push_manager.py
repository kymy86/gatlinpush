import unittest
import json
import config

from app import app
from models import db
from moto import mock_sns

class TestPushManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLLITE
        cls.client = app.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @mock_sns
    def test_create(self):
        """
        Create a new push manager instance
        """
        response = self.client.post(
            '/push/manager/',
            content_type='application/json',
            data=json.dumps({
                'key':'test android key',
                'name':'Test App'
            })
        )
        self.assertEqual(response.status_code, 201)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertTrue('id' in response_json)

    def test_create_with_no_key(self):
        """
        Create a new push manager instance
        with no key value
        """
        response = self.client.post(
            '/push/manager/',
            content_type='application/json',
            data=json.dumps({
                'name':'Test App'
            })
        )
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['message']['key'], 'Firebase key missing')

    def test_create_with_no_name(self):
        """
        Create a new push manager instance
        with no name value
        """
        response = self.client.post(
            '/push/manager/',
            content_type='application/json',
            data=json.dumps({
                'key':'Android key'
            })
        )
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['message']['name'], 'Application name missing')

    def test_create_with_no_params(self):
        """
        Create a new push manager instance
        with no params
        """
        response = self.client.post(
            '/push/manager/',
            content_type='application/json',
            data=json.dumps({})
        )
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertTrue('message' in response_json)

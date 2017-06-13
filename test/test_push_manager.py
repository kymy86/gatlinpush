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

    @mock_sns
    def __create_push_manager(self):
        response = self.client.post(
            '/push/manager/',
            content_type='application/json',
            data=json.dumps({
                'key':'Old android key',
                'name':'Test app'
            })
        )
        return json.loads(response.data.decode('utf-8'))

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

    @mock_sns
    def test_update(self):
        """
        Update an existing push manager instance
        """
        pm = self.__create_push_manager()
        response = self.client.put(
            '/push/manager/'+pm['uuid'],
            content_type='application/json',
            data=json.dumps({
                'key':'New android key'
            })
        )
        response_j2 = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_j2['android_key'], 'New android key')
        self.assertEqual(pm['sns_arn'], response_j2['sns_arn'])

    @mock_sns
    def test_delete(self):
        """
        Delete an existing push manager instance
        """
        pm = self.__create_push_manager()
        response = self.client.delete('/push/manager/'+pm['uuid'])
        self.assertEqual(response.status_code, 200)

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

    @mock_sns
    def test_update_with_not_existing_app(self):
        """
        Update an existing push manager instance
        """
        pm = self.__create_push_manager()
        response = self.client.put(
            '/push/manager/aaaaaa-bbbbb-cccc-cdddddd',
            content_type='application/json',
            data=json.dumps({
                'key':'New android key'
            })
        )
        response_j2 = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_j2['error'], 'App not exist')

    @mock_sns
    def test_get_pm(self):
        pm = self.__create_push_manager()

        response = self.client.get('/push/manager/'+pm['uuid'])
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['app_name'], pm['app_name'])

import unittest
import json
import config

from app import app
from models import db, Installation, PushManager
from moto import mock_sns

class TestInstallation(unittest.TestCase):

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

    def __create_push_manager(self, app_name, a_key):
        response = self.client.post(
            '/push/manager/',
            content_type='application/json',
            data=json.dumps({
                'key':a_key,
                'name':app_name
            })
        )
        return json.loads(response.data.decode('utf-8'))

    def __create_installation(self, app_id, device_id='my-test-device-id'):
        response = self.client.post(
            '/device',
            content_type='application/json',
            data=json.dumps({
                'app_id':app_id,
                'device_id':device_id
            })
        )
        return json.loads(response.data.decode('utf-8'))

    @mock_sns
    def test_get_by_uuid(self):
        pushm = self.__create_push_manager('test app name', "my-test-key")
        ninst = self.__create_installation(pushm['uuid'])
        response = self.client.get('/device/'+ninst['uuid'])
        self.assertEqual(response.status_code, 200)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertTrue(rjson['device_id'], ninst['device_id'])

    def test_get_wrong_deviceid(self):
        response = self.client.get('/device/all/fake-device-id')
        self.assertEqual(response.status_code, 200)

    def test_get_nexist_id(self):
        response = self.client.get('/device/fakeuuid')
        self.assertEqual(response.status_code, 404)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertEqual(rjson['error'], 'installation not exists')

    @mock_sns
    def test_delete_installation(self):
        pushm = self.__create_push_manager('test app name', "my-test-key")
        ninst = self.__create_installation(pushm['uuid'])
        response = self.client.delete('/device/'+ninst['uuid'])
        self.assertEqual(response.status_code, 202)

    @mock_sns
    def teste_delete_all_installation(self):
        pushm = self.__create_push_manager('test app name', "my-test-key")
        self.__create_installation(pushm['uuid'])
        pm2 = self.__create_push_manager('my-aws-app-name-2', 'my-android-key-2')
        self.__create_installation(pm2['uuid'])
        response = self.client.delete('/device/all/my-test-device-id')
        self.assertEqual(response.status_code, 202)
        installations = Installation.query.filter_by(
            device_id='my-test-device-id'
        ).all()
        self.assertTrue(len(installations) == 0)

    @mock_sns
    def test_create_installation(self):
        pushm = self.__create_push_manager('test app name', "my-test-key")
        response = self.client.post(
            '/device',
            content_type='application/json',
            data=json.dumps({
                'app_id':pushm['uuid'],
                'device_id':'my-cool-device-id'
            })
        )
        self.assertEqual(response.status_code, 201)

    @mock_sns
    def test_create_install_no_app(self):
        response = self.client.post(
            '/device',
            content_type='application/json',
            data=json.dumps({
                'app_id':"not-existing-app",
                'device_id':'my-cool-device-id'
            })
        )
        self.assertEqual(response.status_code, 400)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertEqual(rjson['error'], 'App doesn\'t exist')

    @mock_sns
    def test_create_double_install(self):
        pushm = self.__create_push_manager('test app name', "my-test-key")
        self.__create_installation(pushm['uuid'])
        response = self.client.post(
            '/device',
            content_type='application/json',
            data=json.dumps({
                'app_id':pushm['uuid'],
                'device_id':'my-test-device-id'
            })
        )
        self.assertEqual(response.status_code, 400)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertEqual(rjson['error'], 'Duplicate endpoint token: my-test-device-id')

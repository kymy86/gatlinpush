import unittest
import json
import config

from app import app
from models import db, Installation, PushManager

class TestInstallation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLLITE
        cls.client = app.test_client()

    def setUp(self):
        db.create_all()
        self.pm = self.__create_push_manager()
        self.ninst = self.__create_installation()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def __create_push_manager(self):
        pushm = PushManager('my-android-key', 'my-aws-app-name', 'aws-sns-arn')
        return pushm.save()

    def __create_installation(self):
        inst = Installation(self.pm.id, "my-device-id")
        return inst.save()

    def test_get_by_uuid(self):
        response = self.client.get('/device/'+self.ninst.uuid)
        self.assertEqual(response.status_code, 200)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertTrue(rjson['device_id'], self.ninst.device_id)

    def test_get_by_deviceid(self):
        pushm = PushManager('my-android-key-2', 'my-aws-app-name-2', 'aws-sns-arn-2')
        pushm.save()
        inst2 = Installation(pushm.id, 'my-device-id')
        inst2.save()
        response = self.client.get('/device/all/my-device-id')
        self.assertEqual(response.status_code, 200)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(rjson['data']) == 2)

    def test_get_wrong_deviceid(self):
        response = self.client.get('/device/all/fake-device-id')
        self.assertEqual(response.status_code, 200)

    def test_get_nexist_id(self):
        response = self.client.get('/device/fakeuuid')
        self.assertEqual(response.status_code, 404)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertEqual(rjson['error'], 'installation not exists')

    def test_delete_installation(self):
        response = self.client.delete('/device/'+self.ninst.uuid)
        self.assertEqual(response.status_code, 202)
    
    def teste_delete_all_installation(self):
        pushm = PushManager('my-android-key-2', 'my-aws-app-name-2', 'aws-sns-arn-2')
        pushm.save()
        inst2 = Installation(pushm.id, 'my-device-id')
        inst2.save()
        response = self.client.delete('/device/all/my-device-id')
        self.assertEqual(response.status_code, 202)
        installations = Installation.query.filter_by(
            device_id='my-device-id'
        ).all()
        config.logging.debug("#DEBUGGING")
        config.logging.debug(installations)
        self.assertTrue(len(installations) == 0)

    def test_create_installation(self):
        response = self.client.post(
            '/device',
            content_type='application/json',
            data=json.dumps({
                'app_id':self.pm.uuid,
                'device_id':'my-cool-device-id'
            })
        )
        self.assertEqual(response.status_code, 201)

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

    def test_create_double_install(self):
        response = self.client.post(
            '/device',
            content_type='application/json',
            data=json.dumps({
                'app_id':self.pm.uuid,
                'device_id':'my-device-id'
            })
        )
        rows = Installation.query.all()
        self.assertEqual(response.status_code, 400)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertEqual(rjson['error'], 'This device is already registered with this app')

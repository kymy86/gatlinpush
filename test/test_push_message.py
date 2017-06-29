import unittest
import json
import config

from app import app
from models import db, Push, PushManager

class TestPushMessage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLLITE
        cls.client = app.test_client()

    def setUp(self):
        db.create_all()
        self.pushm = self.__create_push_manager()
        self.push = self.__create_push_message()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def __create_push_manager(self):
        pushm = PushManager("App test", 'android-key', 'amazon-sns-arn')
        return pushm.save()

    def __create_push_message(self):
        push = Push("my awesome push", self.pushm.id)
        return push.save()

    def test_get_message(self):

        response = self.client.get('/push/'+self.push.uuid)
        self.assertEqual(response.status_code, 200)
        rjson = json.loads(response.data.decode('utf-8'))
        self.assertTrue(rjson['message'], self.push.message)

    def test_create_message(self):
        response = self.client.post(
            '/push',
            content_type="application/json",
            data=json.dumps({
                'message':'HMy really awesome push',
                'app_id':self.pushm.uuid
            })
        )
        self.assertEqual(response.status_code, 201)


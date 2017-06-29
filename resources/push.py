from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask import url_for, jsonify

from util import parse_params
from repositories import (
    PushManagerRepo,
    PushRepo
)
from util.exceptions import GatlinException
from util.push import send_push
from providers.aws import AwsProvider

class PushSendResource(Resource):

    def post(self, message_id, app_id):
        """
        Send push notification to all
        devices registered in the app
        """
        try:
            push = PushRepo.get_message(message_id, app_id)
            """task = send_push.apply_async(
                args=[push['push'][0]['message'], push['installation']],
                countdown=30
                )"""
            task = send_push.delay(
                push['push'][0]['message'],
                push['installation'],
                push['push'][0]['uuid']
            )
            return {}, 200, {'Location': url_for('push.api.status', task_id=task.id)}
        except GatlinException as e:
            return {"error":str(e.message)}, e.status

class PushStatsResource(Resource):

    def get(self, task_id):
        """
        Return sending status
        """
        task = send_push.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'device_id': 0,
                'message_id':0,
                'total': 1,
                'current':1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'device_id': task.info.get('device_id', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', ''),
                'message_id': task.info.get('message_id', 0)
            }
        else:
            response = {
                'state': task.state,
                'device_id': 0,
                'total': 1,
                'status': str(task.info),
            }
        return jsonify(response)


class PushResource(Resource):

    def get(self, uuid):
        """
        Get a message
        """
        try:
            push = PushRepo.get(uuid)
            return push.json, 200
        except GatlinException as e:
            return {"error":str(e.message)}, e.status

    @parse_params(
        Argument(
            'message',
            location='json',
            required=True,
            help='Push message missing'
        ),
        Argument(
            'app_id',
            location='json',
            required=True,
            help="Application id missing"
        )
    )
    def post(self, message, app_id):
        """
        Save a message
        """
        try:
            push = PushRepo.create(message, app_id)
            return push.json, 201
        except GatlinException as e:
            return {"error":e.message}, e.status

    def put(self, uuid, message):
        """
        @TODO
        """
        pass

    def delete(self, uuid):
        """
        @TODO
        """
        pass


class PushManagerResourceList(Resource):
    """
    Get more than one push manager
    """
    def get(self):
        try:
            push_app = PushManagerRepo.get_all()
            return {"data": [x.json for x in push_app]}, 200
        except GatlinException as e:
            return {"error":e.message}, e.status

class PushManagerResource(Resource):
    """
    Manager push manager creation
    for a given app
    """

    def get(self, uuid):
        try:
            push_app = PushManagerRepo.get(uuid)
            return push_app.json, 200
        except GatlinException as e:
            return {"error":e.message}, e.status

    @parse_params(
        Argument(
            'key',
            location='json',
            required=True,
            help='Firebase key missing'
        ),
        Argument(
            'name',
            location='json',
            required=True,
            help="Application name missing"
        )
    )
    def post(self, key, name):
        try:
            pm = PushManagerRepo(AwsProvider(name))
            push_app = pm.create(key)
            return push_app.json, 201
        except GatlinException as e:
            return {"error":e.message}, e.status

    @parse_params(
        Argument(
            'key',
            location='json',
            required=True,
            help='Firebase key missing'
        )
    )
    def put(self, uuid, key):
        try:
            pm = PushManagerRepo(AwsProvider(None))
            push_app = pm.update(uuid, key)
            return push_app.json, 200
        except GatlinException as e:
            return {"error":e.message}, e.status


    def delete(self, uuid):
        try:
            pm = PushManagerRepo(AwsProvider(None))
            pm.delete(uuid)
            return {}, 202
        except GatlinException as e:
            return {"error":e.message}, e.status

from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask.json import jsonify

from flask import request
from util import parse_params
from repositories.push import PushManagerRepo
from util.exceptions import PushManagerException
from providers.aws import AwsProvider


class PushResource(Resource):

    @staticmethod
    def get():
        return "hello"

class PushManagerResourceList(Resource):
    """
    Get more than one push manager
    """
    def get(self):
        try:
            pm = PushManagerRepo(AwsProvider(None))
            push_app = pm.get_all()
            return {"data": [x.json for x in push_app]}, 200
        except PushManagerException as e:
            return {"error":e.message}, 404

class PushManagerResource(Resource):
    """
    Manager push manager creation
    for a given app
    """

    def get(self, uuid):
        try:
            pm = PushManagerRepo(AwsProvider(None))
            push_app = pm.get(uuid)
            response = jsonify(push_app.json)
            response.status_code = 200
        except PushManagerException as e:
            response = jsonify({'error':e.message})
            response.status_code = 400

        return response

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
        req = request.get_json()
        try:
            pm = PushManagerRepo(AwsProvider(name))
            push_app = pm.create(key)
            return push_app.json, 201
        except PushManagerException as e:
            return {"error":e.message}, 400

    @parse_params(
        Argument(
            'key',
            location='json',
            required=True,
            help='Firebase key missing'
        )
    )
    def put(self, uuid, key):
        req = request.get_json()
        try:
            pm = PushManagerRepo(AwsProvider(None))
            push_app = pm.update(uuid, key)
            response = jsonify(push_app.json)
            response.status_code = 200
        except PushManagerException as e:
            return {"error":e.message}, 400

        return response

    def delete(self, uuid):
        try:
            pm = PushManagerRepo(AwsProvider(None))
            pm.delete(uuid)
            return {}, 202
        except PushManagerException as e:
            return {"error":e.message}, 400

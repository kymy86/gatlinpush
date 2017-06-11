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

class PushManagerResource(Resource):
    """
    Manager push manager creation
    for a given app
    """

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
    def post(self):
        req = request.get_json()
        try:
            pm = PushManagerRepo(AwsProvider(req['name']))
            push_app = pm.create(req['key'])
            response = jsonify(push_app.json)
            response.status_code = 201
        except PushManagerException as e:
            response = jsonify({"error":e.message})
            response.status_code = 400

        return response

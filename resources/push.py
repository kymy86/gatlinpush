from flask_restful import Resource
from flask_restful.reqparse import Argument

from util import parse_params
from repositories.push import PushManagerRepo
from util.exceptions import GatlinException
from providers.aws import AwsProvider


class PushResource(Resource):

    def get(self, uuid):
        #@TODO
        pass

    def post(self, message, app_id):
        pass

    def put(self, uuid, message):
        #@TODO
        pass

    def delete(self, uuid):
        #@TODO
        pass

class PushSendResource(Resource):

    def post(self):
        pass


class PushManagerResourceList(Resource):
    """
    Get more than one push manager
    """
    def get(self):
        try:
            pm = PushManagerRepo(AwsProvider(None))
            push_app = pm.get_all()
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
            pm = PushManagerRepo(AwsProvider(None))
            push_app = pm.get(uuid)
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

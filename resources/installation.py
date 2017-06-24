from flask_restful import Resource
from flask_restful.reqparse import Argument

from util import parse_params
from repositories import InstallationRepo
from util.exceptions import GatlinException
from providers.aws import AwsProvider


class InstallationResourceList(Resource):

    def get(self, deviceid):
        """
        GET: /device/all/<string:deviceid>
        Return a json list with all installation
        """
        try:
            installation = InstallationRepo.get_by_deviceid(deviceid)
            return {'data':[i.json for i in installation]}, 200
        except GatlinException as e:
            return {"error":e.message}, e.status

    def delete(self, deviceid):
        """
        DELETE /device/all/<string:deviceid>
        Delete all installation
        """
        try:
            irepo = InstallationRepo(AwsProvider(None))
            irepo.delete_by_deviceid(deviceid)
            return {}, 202
        except GatlinException as e:
            return {"error":e.message}, e.status

class InstallationResource(Resource):

    def get(self, uuid):
        """
        GET /device/<string:uuid>
        return one single installation
        """

        try:
            installation = InstallationRepo.get(uuid)
            return installation.json, 200
        except GatlinException as e:
            return {"error":e.message}, e.status

    @parse_params(
        Argument(
            'app_id',
            location='json',
            required=True,
            help="App id is required"
        ),
        Argument(
            'device_id',
            location='json',
            required=True,
            help="Device id is required"
        )
    )
    def post(self, app_id, device_id):
        """
        POST /device
        body {
            "app_id":"app_id",
            "devivice_id":"device_id"
        }
        Create a  new installation
        """
        try:
            irepo = InstallationRepo(AwsProvider(None))
            installation = irepo.create(device_id, app_id)
            return installation.json, 201
        except GatlinException as e:
            return {"error":e.message}, e.status

    def delete(self, uuid):
        """
        DELETE /device/<string:uuid>
        Delete a particular installation
        """
        try:
            irepo = InstallationRepo(AwsProvider(None))
            irepo.delete(uuid)
            return {}, 202
        except GatlinException as e:
            return {"error":e.message}, e.status
        
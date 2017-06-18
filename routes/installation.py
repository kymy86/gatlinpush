from flask import Blueprint
from flask_restful import Api

from resources import InstallationResource, InstallationResourceList

INST_BLUEPRINT = Blueprint('installation', __name__)
Api(INST_BLUEPRINT).add_resource(
    InstallationResource,
    '/device/<string:uuid>',
    '/device',
    strict_slashes=False
)

Api(INST_BLUEPRINT).add_resource(
    InstallationResourceList,
    '/device/all/<string:deviceid>',
    strict_slashes=False
)

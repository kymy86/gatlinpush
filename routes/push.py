from flask import Blueprint
from flask_restful import Api

from resources import (
    PushResource,
    PushManagerResource,
    PushManagerResourceList,
    PushSendResource
)


PUSH_BLUEPRINT = Blueprint('push', __name__)
Api(PUSH_BLUEPRINT).add_resource(
    PushManagerResource,
    '/push/manager',
    '/push/manager/<string:uuid>',
    strict_slashes=False
)
Api(PUSH_BLUEPRINT).add_resource(
    PushManagerResourceList,
    '/push/manager/all',
    strict_slashes=False
)
Api(PUSH_BLUEPRINT).add_resource(
    PushResource,
    '/push',
    '/push/<string:uuid>',
    strict_slashes=False
)
Api(PUSH_BLUEPRINT).add_resource(
    PushSendResource,
    '/push/send/<string:uuid>',
    strict_slashes=False
)

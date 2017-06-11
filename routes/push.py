from flask import Blueprint
from flask_restful import Api

from resources import PushResource, PushManagerResource


PUSH_BLUEPRINT = Blueprint('push', __name__)
Api(PUSH_BLUEPRINT).add_resource(
    PushManagerResource,
    '/push/manager/'
)
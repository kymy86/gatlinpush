import re
from models import (
    Push,
    PushManager,
)
from util.exceptions import GatlinException
from providers.abc import Provider
from sqlalchemy.exc import IntegrityError


class PushRepo:

    @staticmethod
    def get(uuid):
        push = Push.query.filter_by(
            uuid=uuid
        ).one_or_none()



class PushManagerRepo:

    def __init__(self, provider):
        """
        Instantiate the provider
        """
        if isinstance(provider, Provider):
            self._provider = provider
        else:
            raise GatlinException("Invalid Provider", 400)

    def get(self, uuid):
        """
        Get a push manager
        """
        pmanager = PushManager.query.filter_by(
            uuid=uuid
        ).one_or_none()
        if pmanager is None:
            raise GatlinException("App not exist", 404)
        return pmanager

    def get_all(self):
        """
        Get all the push manager
        """
        return PushManager.query.all()


    def create(self, android_key):
        """
        Create a new push manager
        """
        try:
            sns_arn = self._provider.set_android_platform(android_key)
            push_manager = PushManager(android_key, self._provider.app_name, sns_arn)
            return push_manager.save()
        except GatlinException as exception:
            raise exception
        except IntegrityError:
            raise GatlinException("Error while saving the app", 400)

    def update(self, uuid, android_key):
        """
        Update the android key of the
        given push manager
        """
        try:
            pmanager = PushManager.query.filter_by(
                uuid=uuid
            ).one_or_none()
            if pmanager is None:
                raise GatlinException("App not exist", 404)
            self._provider.app_name = pmanager.app_name
            sns_arn = self._provider.set_android_platform(android_key)
            pmanager.android_key = android_key
            return pmanager.save()
        except GatlinException as exception:
            raise exception

    def delete(self, uuid):
        """
        Remove a push manager
        """
        try:
            pmanager = PushManager.query.filter_by(
                uuid=uuid
            ).one_or_none()
            if pmanager is None:
                raise GatlinException("App not exist", 404)
            self._provider.delete_platform(pmanager.sns_arn)
            pmanager.delete()
        except GatlinException as exception:
            raise exception

import re
from models import (
    Push,
    PushManager,
)
from util.exceptions import PushManagerException
from providers.abc import Provider
from sqlalchemy.exc import IntegrityError

class PushManagerRepo:

    def __init__(self, provider):
        """
        Instantiate the provider
        """
        if isinstance(provider, Provider):
            self._provider = provider
        else:
            raise PushManagerException("Invalid Provider")

    def get(self, uuid):
        """
        Get a push manager
        """
        pmanager = PushManager.query.filter_by(
            uuid=uuid
        ).one_or_none()
        if pmanager is None:
            raise PushManagerException("App not exist")
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
        except PushManagerException as exception:
            raise exception
        except IntegrityError:
            raise PushManagerException("Error while saving the app")

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
                raise PushManagerException("App not exist")
            self._provider.app_name = pmanager.app_name
            sns_arn = self._provider.set_android_platform(android_key)
            pmanager.android_key = android_key
            return pmanager.save()
        except PushManagerException as exception:
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
                raise PushManagerException("App not exist")
            self._provider.delete_platform(pmanager.sns_arn)
            pmanager.delete()
        except PushManagerException as exception:
            raise exception

import re
from models import (
    Push,
    PushManager
)
from util.exceptions import PushManagerException
from providers.abc import Provider

class PushRepo:
    pass

class PushManagerRepo:
    """
    1. Create a push manager record
    2. Crreate an android app with SNS
    3. Return success
    """
    def __init__(self, provider):
        if isinstance(provider, Provider):
            self._provider = provider
        else:
            raise PushManagerException("Invalid Provider")


    def create(self, android_key):
        try:
            sns_arn = self._provider.set_android_platform(android_key)
        except PushManagerException:
            raise PushManagerException

        push_manager = PushManager(android_key, self._provider.app_name, sns_arn)
        return push_manager.save()
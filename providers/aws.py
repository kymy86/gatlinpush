import re
from config import sns_client, logging
from botocore.exceptions import ClientError
from util.exceptions import GatlinException
from .abc import Provider

class AwsProvider(Provider):

    def __init__(self, app_name):
        if app_name is not None:
            self._app_name = self.__clean_param(app_name)
        else:
            self._app_name = ""

    def __clean_param(self, app_name):
        """
        Clean the app name so
        it's compliant with Amazon SNS
        specifications
        """
        re1 = re.compile(r"[^a-zA-Z0-9\-_\.]+")
        return re1.sub("-", app_name)

    @property
    def provider_name(self):
        return "AWS"

    @property
    def app_name(self):
        return self._app_name

    @app_name.setter
    def app_name(self, app_name):
        self._app_name = self.__clean_param(app_name)

    def set_android_platform(self, android_key):

        try:
            response = sns_client.create_platform_application(
                Name=self._app_name,
                Platform="GCM",
                Attributes={
                    "PlatformCredential":android_key
                }
            )
            return response['PlatformApplicationArn']
        except ClientError as e:
            raise GatlinException(e.response['Error']['Message'], 400)

    def delete_platform(self, platform_id):

        try:
            sns_client.delete_platform_application(
                PlatformApplicationArn=platform_id
            )
        except ClientError as e:
            raise GatlinException(e.response['Error']['Message'], 400)

    def create_endpoint(self, device_id, platform_id):

        try:
            response = sns_client.create_platform_endpoint(
                PlatformApplicationArn=platform_id,
                Token=device_id
            )
            return response['EndpointArn']
        except ClientError as err:
            raise GatlinException(err.response['Error']['Message'], 400)

    def set_ios_platoform(self):
        pass

    def delete_endpoint(self, platform_id):
        try:
            response = sns_client.delete_endpoint(
                EndpointArn=platform_id
            )
        except ClientError as e:
            raise GatlinException(e.response['Error']['Message'], 400)
    
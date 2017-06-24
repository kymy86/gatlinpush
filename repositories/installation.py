from models import Installation, PushManager
from util.exceptions import GatlinException
from sqlalchemy.exc import IntegrityError
from providers.abc import Provider

class InstallationRepo:


    def __init__(self, provider):
        """
        Instantiate the provider
        """
        if isinstance(provider, Provider):
            self._provider = provider
        else:
            raise GatlinException("Invalid Provider", 400)

    @staticmethod
    def get(uuid):
        """
        Return one installation for a given
        uuid
        """

        installation = Installation.query.filter_by(
            uuid=uuid
        ).one_or_none()
        if installation is None:
            raise GatlinException("installation not exists", 404)
        return installation

    @staticmethod
    def get_by_deviceid(deviceid):
        """
        Return multiple installation for the given
        device_id
        """
        installation = Installation.query.filter_by(
            device_id=deviceid
        ).all()
        return installation

    def delete_by_deviceid(self, deviceid):
        """
        Delete all installations for the given
        device_id
        """
        installations = Installation.query.filter_by(
            device_id=deviceid
        ).all()
        if len(installations) > 0:
            try:
                for i in installations:
                    self._provider.delete_endpoint(i.endpoint_arn)
                    i.delete()
            except GatlinException as iexc:
                return iexc

    def delete(self, uuid):
        """
        Delete one particular installation
        """
        installation = Installation.query.filter_by(
            uuid=uuid
        ).one_or_none()
        if installation is None:
            raise GatlinException("Installation not exists", 404)
        try:
            self._provider.delete_endpoint(installation.endpoint_arn)
            installation.delete()
        except GatlinException as iexc:
            return iexc

    def create(self, device_id, app_id):
        """
        app_id is the uuid
        device_id id generated by the android/ios device
        """
        pm = PushManager.query.filter_by(
            uuid=app_id
        ).one_or_none()
        if pm is None:
            raise GatlinException("App doesn't exist", 400)
        try:
            endpoint_arn = self._provider.create_endpoint(device_id, pm.sns_arn)
            installation = Installation(pm.id, device_id, endpoint_arn)
            return installation.save()
        except GatlinException as iexc:
            raise iexc
        except IntegrityError as ie:
            raise GatlinException("This device is already registered with this app", 400)

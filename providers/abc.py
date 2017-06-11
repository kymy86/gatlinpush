from abc import ABCMeta, abstractmethod

class Provider(metaclass=ABCMeta):


    @abstractmethod
    def set_android_platform(self, android_key):
        pass

    @abstractmethod
    def set_ios_platoform(self):
        pass

    @property
    def app_name(self):
        pass

    @app_name.setter
    def app_name(self, app_name):
        self._app_name_setter(app_name)

    @abstractmethod
    def _app_name_setter(self, app_name):
        pass

    @property
    def provider_name(self):
        pass

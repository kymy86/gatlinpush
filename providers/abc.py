from abc import ABCMeta, abstractmethod

class Provider(metaclass=ABCMeta):


    @abstractmethod
    def set_android_platform(self, android_key):
        pass

    @abstractmethod
    def set_ios_platoform(self):
        pass

    @abstractmethod
    def delete_platform(self, platform_id):
        pass

    @property
    def provider_name(self):
        pass

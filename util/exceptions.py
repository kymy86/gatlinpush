
class PushManagerException(Exception):

    def __init__(self, message):
        super(PushManagerException, self).__init__(message)
        self.message = message

class InstallationException(Exception):

    def __init__(self, message, status):
        super(InstallationException, self).__init__(message)
        self.message = message
        self.status = status

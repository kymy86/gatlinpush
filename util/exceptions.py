
class PushManagerException(Exception):

    def __init__(self, message):
        super(PushManagerException, self).__init__(message)
        self.message = message

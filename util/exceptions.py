
class GatlinException(Exception):

    def __init__(self, message, status):
        super(GatlinException, self).__init__(message)
        self.message = message
        self.status = status

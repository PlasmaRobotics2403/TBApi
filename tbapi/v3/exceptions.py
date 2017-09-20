"""TBApi v3 Exceptions"""

class InvalidRequestError(Exception):
    """EXCEPTION: Invalid Data Request"""
    def __init__(self):
        Exception.__init__(self, 'Invalid Data Request')

class InvalidKeyError(Exception):
    """EXCEPTION: Data Key does not exist"""
    def __init__(self):
        Exception.__init__(self, 'Data Key does not exist')

class OfflineError(Exception):
    """Exception: Connection to The Blue Alliance could not be completed"""
    def __init__(self):
        Exception.__init__(self, 'Connection to The Blue Alliance could not be completed')
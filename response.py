import struct
from enum import Enum


class ResponseCode(Enum):
    REGISTER_SUCCESS = 200
    REGISTER_FAILURE = 201
    INTERNAL_SERVER_ERROR = 1000


"""Class for representing a response"""


class Response:
    def __init__(self, code, payload=None):
        self.code = code
        if payload != None:
            self.payload = payload
            self.payload_size = len(self.payload)
        else:
            self.payload = None
            self.payload_size = 0

    @staticmethod
    def register_failure():
        # No payload for REGISTER_FAILURE
        return Response(ResponseCode.REGISTER_FAILURE)

    @staticmethod
    def register_success(client_id):
        return Response(ResponseCode.REGISTER_SUCCESS)

    @staticmethod
    def internal_error():
        return Response(ResponseCode.INTERNAL_SERVER_ERROR)

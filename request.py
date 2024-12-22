from enum import Enum


class Op(Enum):
    RECONNECT = 100
    REGISTER = 101


class Payload:
    pass


class PublicKeyPayload(Payload):
    def __init__(self, public_key):
        self.public_key = public_key

    def get_public_key(self):
        return self.public_key


class Request:
    def __init__(self, phone_id, dest_phone_id, opcode, timestamp, payload: Payload):
        self.phone_id = phone_id
        self.dest_phone_id = dest_phone_id
        self.opcode = opcode
        self.timestamp = timestamp
        self.payload = payload

    def get_code(self) -> Op:
        return self.opcode

    def get_phone_id(self):
        return self.phone_id

    def get_dest_phone_id(self):
        return self.dest_phone_id

    def get_timestamp(self):
        return self.timestamp

    def get_payload(self):
        return self.payload

    def __str__(self):
        output = f"""Incoming Request :
        Phone ID = {self.phone_id}
        Destination phone = {self.dest_phone_id}
        OP = {self.opcode}
        Timestamp = {self.timestamp}
        Raw payload = {self.payload}"""
        return output

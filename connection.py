
import socket
import struct
from cryptomanager import *
from request import *
from response import *

FIXED_HEADER_SIZE = 256
RSA_KEY_LEN = 256
"""This class serves for handling the connection with the clients. Each session with client is associated with a unique connection object through which the communication is done."""


class Connection:

    def __init__(self, sock: socket.socket, crypto: CryptoManager):
        self.sock = sock
        self.crypto = crypto

    def read_request(self):
        """This method returns a request read from client"""
        if self.sock is None:
            raise ConnectionError("Connection is not open")

        try:
            encrypted_header = self.sock.recv(FIXED_HEADER_SIZE)
        except ConnectionResetError:
            raise ConnectionResetError("Connection Reset Error")

        if len(encrypted_header) == 0:
            raise Exception("Connection closed by peer")

        if len(encrypted_header) < FIXED_HEADER_SIZE:
            raise ValueError(
                f"Expected {FIXED_HEADER_SIZE} bytes, but got {len(data)}")

        # TODO: decrypt header
        data = self.crypto.decrypt_with_private_key(encrypted_header)
        # Unpack
        phone_id, dest_phone_id, code, timestamp, payload_size = struct.unpack(
            '<10s 10s B 4s I', data)

        # convert code to Enum type
        code = Op(code)
        if (code == Op.REGISTER):
            # Check if payload size is correct according to the protocol
            if (payload_size == RSA_KEY_LEN):
                payload = PublicKeyPayload(self.sock.recv(RSA_KEY_LEN))
            else:
                print("Payload size does not correspond to the expected size")

        return Request(phone_id, dest_phone_id, code, timestamp, payload)

    def close(self):
        # Close the socket
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_response(self, response: Response):
        """This method receives a response as an argument and sends it to the client"""
        if self.sock is None:
            raise ConnectionError("Connection is not open")

        # send the serialized response
        self.sock.sendall(response.to_bytes())


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
            encrypted_header = self.sock.recv(RSA_KEY_LEN)
        except ConnectionResetError:
            raise ConnectionResetError("Connection Reset Error")

        if len(encrypted_header) == 0:
            raise Exception("Connection closed by peer")

        if len(encrypted_header) < RSA_KEY_LEN:
            raise ValueError(
                f"Expected {RSA_KEY_LEN} bytes, but got {len(encrypted_header)}")

        # TODO: decrypt header
        decrypted_header = self.crypto.decrypt_with_private_key(
            encrypted_header)
        # Unpack
        phone_id, dest_phone_id, code, timestamp, payload_size = struct.unpack(
            '<10s 10s B I I', decrypted_header)

        print(f"""Decrypted header :
              Phone id = {phone_id}, Dest = {dest_phone_id}, Code = {code}, Timestamp = {int(timestamp)}, Payload Size = {payload_size}""")

        # Read payload
        encrypted_payload = self.sock.recv(RSA_KEY_LEN)
        # Read hash
        encrypted_hash = self.sock.recv(RSA_KEY_LEN)
        # Decrypt payload
        decrypted_payload = self.crypto.decrypt_with_private_key(
            encrypted_payload)
        print(f"Decrypted payload = ", decrypted_payload)
        # Decrypt hash
        decrypted_hash = self.crypto.decrypt_with_private_key(encrypted_hash)
        print(f"Decrypted hash = ", decrypted_hash)
        # ------------------- Calculate hash and compare ---------------------------
        computed_hash = self.crypto.compute_SHA256(
            decrypted_header, decrypted_payload)
        print("Computed hash = ", computed_hash)
        if (computed_hash == decrypted_hash):
            print("Hash match !")

        # drop request if hash is bad other wise continue below
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

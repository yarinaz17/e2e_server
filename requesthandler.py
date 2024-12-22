import uuid
import os
import copy
from request import *
from response import *
from server import *
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad

"""This RequestHandler class is used to handle the different requests supported by the protocol"""


class RequestHandler:
    def __init__(self):
        pass

    def handle_request(self, request: Request, user: User):
        """This method receives a request and a User object as argument and invokes the right request handler based on the request code"""
        code = request.get_code()
        # Update last seen for user
        if code == Op.REGISTER:
            print("[SERVER] Incoming registration request from peer.")
            return self.handle_register(request)
        # check if user is trying to perform operations without being registered
        elif code == Op.RECONNECT:
            print("[SERVER] Incoming reconnect request from peer")
            return self.handle_reconnect(request)
        else:
            return Response.internal_error()

    def handle_register(self, request: Request):
        """This method receives a registration request and registers the user within the database and generates a UUID for him"""
        # check if user is already registered
        if request.get_phone_id() in [v for v in Server.clients]:
            return Response.register_failure()

        Server.clients.append(request.get_phone_id())
        return Response.register_success()

    def handle_reconnect(self, request):
        pass

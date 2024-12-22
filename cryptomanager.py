from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256


class CryptoManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of CryptoManager exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            # Perform any necessary initialization here
        return cls._instance

    def __init__(self):
        with open("public.pem", "rb") as public_key_file:
            self.public_key = RSA.importKey(public_key_file.read())

        with open("private.pem", "rb") as private_key_file:
            self.key_pair = RSA.importKey(private_key_file.read())

    def encrypt_with_public_key(self, data):
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_data = cipher_rsa.encrypt(data)
        return encrypted_data

    def decrypt_with_private_key(self, encrypted_data):
        cipher_rsa = PKCS1_OAEP.new(self.key_pair)
        data = cipher_rsa.decrypt(encrypted_data)
        return data

    def compute_SHA256(self, header, payload):
        hash_obj = SHA256.new()
        hash_obj.update(header+payload)
        return hash_obj.digest()

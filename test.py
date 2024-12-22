from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad


if __name__ == "__main__":
    key_pair = RSA.generate(2048)
    public_key = key_pair.publickey()

    # Import keys
    with open("public.pem", "rb") as public_key_file:
        public_key = RSA.importKey(public_key_file.read())

    with open("private.pem", "rb") as private_key_file:
        key_pair = RSA.importKey(private_key_file.read())

    # encryption
    MESSAGE = b'550011'
    scrambler = PKCS1_OAEP.new(public_key)
    encrypted = scrambler.encrypt(MESSAGE)
    # --------------------------------------------------------------
    # decryption
    descrambler = PKCS1_OAEP.new(key_pair)
    decrypted = descrambler.decrypt(encrypted)
    # --------------------------------------------------------------

    print("Encrypted:", encrypted)
    print("Encrypted len:", len(encrypted))
    print("Decrypted:", decrypted)

    # --------------------------------------------------------------
    print("DER length: ", len(public_key.export_key(format='DER')))

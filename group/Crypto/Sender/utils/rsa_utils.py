from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def encrypt_rsa_key(public_key_file: str, data: bytes) -> bytes:
    pub_key = RSA.import_key(open(public_key_file).read())
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(data)

def decrypt_rsa_key(private_key_file: str, encrypted_data: bytes) -> bytes:
    priv_key = RSA.import_key(open(private_key_file).read())
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(encrypted_data)

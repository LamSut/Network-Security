from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_aes(plaintext: str):
    key = get_random_bytes(16)  # AES-128
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return key, cipher.nonce, ciphertext, tag

def decrypt_aes(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

from utils.aes_utils import encrypt_aes
from utils.rsa_utils import encrypt_rsa_key
import base64

# Load message
with open("message.txt", "r") as file:
    message = file.read()

# Encrypt with AES
aes_key, nonce, ciphertext, tag = encrypt_aes(message)

# Encrypt AES key with RSA
encrypted_key = encrypt_rsa_key("keys/public.pem", aes_key)

# Save encrypted data to files
with open("../Receiver/encrypted_mess/encrypted_key.bin", "wb") as f: f.write(encrypted_key)
with open("../Receiver/encrypted_mess/ciphertext.bin", "wb") as f: f.write(ciphertext)
with open("../Receiver/encrypted_mess/nonce.bin", "wb") as f: f.write(nonce)
with open("../Receiver/encrypted_mess/tag.bin", "wb") as f: f.write(tag)

print("Message encrypted successfully.")

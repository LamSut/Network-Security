from utils.aes_utils import decrypt_aes
from utils.rsa_utils import decrypt_rsa_key

# Load encrypted data
with open("encrypted_mess/encrypted_key.bin", "rb") as f: encrypted_key = f.read()
with open("encrypted_mess/ciphertext.bin", "rb") as f: ciphertext = f.read()
with open("encrypted_mess/nonce.bin", "rb") as f: nonce = f.read()
with open("encrypted_mess/tag.bin", "rb") as f: tag = f.read()

# Decrypt AES key using RSA
aes_key = decrypt_rsa_key("keys/private.pem", encrypted_key)

# Decrypt message using AES
plaintext = decrypt_aes(aes_key, nonce, ciphertext, tag)

print("Decrypted Message:")
print(plaintext)

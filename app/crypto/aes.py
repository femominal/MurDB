from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
def generate_aes_key() -> bytes:
    return get_random_bytes(32)
def encrypt_data(aes_key: bytes, plaintext: bytes):
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce, ciphertext, tag
def decrypt_data(aes_key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes):
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

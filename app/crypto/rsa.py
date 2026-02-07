from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
def generate_rsa_keypair(key_size: int = 3072):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key
def encrypt_key_with_rsa(public_key_bytes: bytes, data: bytes) -> bytes:
    public_key = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    return cipher.encrypt(data)
def decrypt_key_with_rsa(private_key_bytes: bytes, encrypted_data: bytes) -> bytes:
    private_key = RSA.import_key(private_key_bytes)
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    return cipher.decrypt(encrypted_data)

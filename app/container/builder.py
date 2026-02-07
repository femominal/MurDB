import struct
from app.container.format import MAGIC, VERSION
def build_container(encrypted_key: bytes, nonce: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    container = bytearray()
    container += MAGIC
    container += struct.pack("B", VERSION)
    # Длина RSA-ключа
    container += struct.pack(">H", len(encrypted_key))
    container += encrypted_key
    # NONCE
    container += struct.pack(">H", len(nonce))
    container += nonce
    # TAG
    container += struct.pack(">H", len(tag))
    container += tag
    # DATA
    container += struct.pack(">I", len(ciphertext))
    container += ciphertext
    return bytes(container)

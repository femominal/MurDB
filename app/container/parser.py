import struct
from app.container.format import MAGIC
def parse_container(data: bytes):
    offset = 0
    # MAGIC
    if data[:6] != MAGIC:
        raise ValueError("Invalid container format")

    offset += 6
    # VERSION
    version = data[offset]
    offset += 1
    # RSA encrypted key
    key_len = struct.unpack(">H", data[offset:offset+2])[0]
    offset += 2
    encrypted_key = data[offset:offset+key_len]
    offset += key_len
    # NONCE
    nonce_len = struct.unpack(">H", data[offset:offset+2])[0]
    offset += 2
    nonce = data[offset:offset+nonce_len]
    offset += nonce_len
    # TAG
    tag_len = struct.unpack(">H", data[offset:offset+2])[0]
    offset += 2
    tag = data[offset:offset+tag_len]
    offset += tag_len
    # DATA
    data_len = struct.unpack(">I", data[offset:offset+4])[0]
    offset += 4
    ciphertext = data[offset:offset+data_len]
    return {
        "version": version,
        "encrypted_key": encrypted_key,
        "nonce": nonce,
        "tag": tag,
        "ciphertext": ciphertext,
    }

from app.crypto.aes import generate_aes_key, encrypt_data
from app.crypto.rsa import encrypt_key_with_rsa
from app.container.builder import build_container
from app.exporter.sqlite import export_sqlite_db
from app.services.key_service import load_public_key
from app.exporter.sqlite import export_sqlite_db
from app.exporter.postgres import export_postgres_db
from app.exporter.mongodb import export_mongodb_db

def secure_export(db_type: str, db_name: str) -> bytes:
    if db_type == "sqlite":
        dump_data = export_sqlite_db(db_name)
    elif db_type == "postgres":
        dump_data = export_postgres_db(db_name)
    elif db_type == "mongodb":
        dump_data = export_mongodb_db(db_name)
    else:
        raise ValueError("Unsupported database type")

    aes_key = generate_aes_key()
    nonce, ciphertext, tag = encrypt_data(aes_key, dump_data)

    public_key = load_public_key()
    encrypted_key = encrypt_key_with_rsa(public_key, aes_key)

    container = build_container(encrypted_key, nonce, tag, ciphertext)
    return container

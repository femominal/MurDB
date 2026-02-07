import os
from pathlib import Path
from app.crypto.rsa import generate_rsa_keypair
DEFAULT_KEY_DIR = Path.home() / ".MurDB"
def ensure_key_dir():
    DEFAULT_KEY_DIR.mkdir(parents=True, exist_ok=True)
def generate_and_store_keys(key_size: int = 3072):
    ensure_key_dir()
    private_key, public_key = generate_rsa_keypair(key_size)
    private_path = DEFAULT_KEY_DIR / "private.pem"
    public_path = DEFAULT_KEY_DIR / "public.pem"
    with open(private_path, "wb") as f:
        f.write(private_key)
    with open(public_path, "wb") as f:
        f.write(public_key)
    os.chmod(private_path, 0o600)
    return private_path, public_path
def load_private_key(path: str | None = None) -> bytes:
    if path is None:
        path = DEFAULT_KEY_DIR / "private.pem"
    with open(path, "rb") as f:
        return f.read()
def load_public_key(path: str | None = None) -> bytes:
    if path is None:
        path = DEFAULT_KEY_DIR / "public.pem"
    with open(path, "rb") as f:
        return f.read()

import argparse
import subprocess
import requests
import sys
from pathlib import Path

from app.crypto.rsa import generate_rsa_keypair

API_URL = "http://localhost:8000/export"
API_KEY = "dev-secret-key"

KEY_DIR = Path.home() / ".MurDB"
PRIVATE_KEY = KEY_DIR / "private.pem"
PUBLIC_KEY = KEY_DIR / "public.pem"


# =============================
# KEY GENERATION (LOCAL)
# =============================

def cmd_keygen():
    KEY_DIR.mkdir(exist_ok=True)

    if PRIVATE_KEY.exists() or PUBLIC_KEY.exists():
        print("⚠ Keys already exist.")
        return

    priv, pub = generate_rsa_keypair()

    PRIVATE_KEY.write_bytes(priv)
    PUBLIC_KEY.write_bytes(pub)

    print(f"Private key saved to: {PRIVATE_KEY}")
    print(f"Public key saved to: {PUBLIC_KEY}")


# =============================
# DOCKER MANAGEMENT
# =============================

def cmd_up():
    subprocess.run(["docker", "compose", "up", "-d"], check=False)


def cmd_down():
    subprocess.run(["docker", "compose", "down"], check=False)


def cmd_status():
    subprocess.run(["docker", "compose", "ps"], check=False)


# =============================
# EXPORT
# =============================

def cmd_export(db_type, db_name):
    if not PUBLIC_KEY.exists():
        print("❌ No public key found. Run: murdb keygen")
        sys.exit(1)

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "db_type": db_type,
        "db_name": db_name
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Run: murdb up")
        sys.exit(1)

    if response.status_code == 200:
        filename = f"{db_name}.sq"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✓ Backup saved as {filename}")
    else:
        print("❌ Export failed:", response.text)
        sys.exit(1)


# =============================
# DECRYPT (LOCAL)
# =============================

def cmd_decrypt(file_path):
    if not PRIVATE_KEY.exists():
        print("❌ No private key found.")
        sys.exit(1)

    subprocess.run(
        ["python", "-m", "cli.cli", "decrypt", file_path],
        check=False
    )


# =============================
# CLI PARSER
# =============================

def build_parser():
    parser = argparse.ArgumentParser(
        prog="murdb",
        description="MurDB - Secure Database Export Tool"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("keygen")
    sub.add_parser("up")
    sub.add_parser("down")
    sub.add_parser("status")

    export_parser = sub.add_parser("export")
    export_parser.add_argument("--type", required=True)
    export_parser.add_argument("--db", required=True)

    decrypt_parser = sub.add_parser("decrypt")
    decrypt_parser.add_argument("file")

    return parser


# =============================
# ENTRY POINT
# =============================

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "keygen":
        cmd_keygen()

    elif args.command == "up":
        cmd_up()

    elif args.command == "down":
        cmd_down()

    elif args.command == "status":
        cmd_status()

    elif args.command == "export":
        cmd_export(args.type, args.db)

    elif args.command == "decrypt":
        cmd_decrypt(args.file)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
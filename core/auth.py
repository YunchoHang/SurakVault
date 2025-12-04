import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Path where you can store salt kkkkkkkkk
SALT_FILE = "data/salt.bin"

# just to make sure that folder xa ke xaina vanera
os.makedirs("data", exist_ok=True)

#  existing salt lai use garxa or creates a new one
def load_or_create_salt():
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)  # generate jpt 16-byte salt
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt

# Derive AES key from master password
def derive_key(master_password: str) -> bytes:
    """
    Derives a 32-byte AES key from the master password using PBKDF2-HMAC-SHA256.
    """
    salt = load_or_create_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000
    )
    return kdf.derive(master_password.encode())

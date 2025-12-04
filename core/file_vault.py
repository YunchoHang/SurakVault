import os
import shutil
from core.crypto import encrypt, decrypt

VAULT_DIR = "data/encrypted_files"
ORIGINAL_DIR = "data/original_files"

#directories xa ke xaina vanera herxa
os.makedirs(VAULT_DIR, exist_ok=True)
os.makedirs(ORIGINAL_DIR, exist_ok=True)

def encrypt_file(key, file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError("File does not exist!")

    filename = os.path.basename(file_path)
    enc_filename = f"encrypted_{filename}.bin"
    enc_path = os.path.join(VAULT_DIR, enc_filename)

    with open(file_path, "rb") as f:
        plaintext = f.read()

    ciphertext = encrypt(key, plaintext)

    #encrypted file lai save garne
    with open(enc_path, "wb") as f:
        f.write(ciphertext)

    #Move og file to ORIGINAL_DIR
    shutil.move(file_path, os.path.join(ORIGINAL_DIR, filename))

    return enc_path

def decrypt_file(key, enc_path, save_path):
    if not os.path.isfile(enc_path):
        raise FileNotFoundError("Encrypted file not found!")

    with open(enc_path, "rb") as f:
        ciphertext = f.read()

    plaintext = decrypt(key, ciphertext)

    with open(save_path, "wb") as f:
        f.write(plaintext)

def reencrypt_file_vault(old_key, new_key):
    #if master password change hunxa teti khere Re-encrypt all encrypted files.
    for f in os.listdir(VAULT_DIR):
        full_path = os.path.join(VAULT_DIR, f)
        if os.path.isfile(full_path) and f.endswith(".bin"):
            with open(full_path, "rb") as file:
                ciphertext = file.read()
            plaintext = decrypt(old_key, ciphertext)
            new_ciphertext = encrypt(new_key, plaintext)
            with open(full_path, "wb") as file:
                file.write(new_ciphertext)

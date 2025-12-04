import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# Key derivation from password
def derive_key(password: str, salt: bytes = None) -> bytes:
    """
    Derive a 32-byte AES key from the given password using PBKDF2.
    If no salt is provided, It will generate a fixed salt for simplicity.
    """
    if salt is None:
        # For simplicity, It uses a fixed salt and for production, it store the salt securely in a file.
        salt = b"securevault_salt"
    return PBKDF2(password, salt, dkLen=32, count=100_000)

# AES encryption
def encrypt(key: bytes, plaintext: bytes) -> bytes:
    #Encrypts plaintext using AES-GCM.
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce + tag + ciphertext

# AES decryption
def decrypt(key: bytes, enc: bytes) -> bytes:
    #Decrypts data encrypted with AES-GCM.
    nonce = enc[:16]
    tag = enc[16:32]
    ciphertext = enc[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

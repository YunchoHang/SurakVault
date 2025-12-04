import json
import os
from core.crypto import encrypt, decrypt

VAULT_FILE = "data/password_vault.enc"

# Load vault from file
def load_vault(key):
    if not os.path.exists(VAULT_FILE):
        return []  # empty list for UI

    with open(VAULT_FILE, "rb") as f:
        enc = f.read()

    dec = decrypt(key, enc)
    vault_dict = json.loads(dec.decode())

    # basically entries haru lai list garne
    entries = []
    for website, data in vault_dict.items():
        entries.append({
            "website": website,
            "username": data["username"],
            "password": data["password"]
        })
    return entries

# Save vault to file
def save_vault(key, entries):

    vault_dict = {entry["website"]: {"username": entry["username"], "password": entry["password"]} for entry in entries}

    plaintext = json.dumps(vault_dict).encode()
    enc = encrypt(key, plaintext)

    os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)
    with open(VAULT_FILE, "wb") as f:
        f.write(enc)

# Add or update entry
def add_entry(key, website, username, password):
    entries = load_vault(key)
    # check if website is there or not?? khasai dup rakhnu parne ho idk what to do.
    for entry in entries:
        if entry["website"] == website:
            entry["username"] = username
            entry["password"] = password
            break
    else:
        entries.append({
            "website": website,
            "username": username,
            "password": password
        })
    save_vault(key, entries)

# Delete an entry by index
def delete_entry(key, index):
    entries = load_vault(key)
    if 0 <= index < len(entries):
        entries.pop(index)
        save_vault(key, entries)
    else:
        raise IndexError("Invalid index")

# Get all entries (optional helper)
def get_all_entries(key):
    return load_vault(key)

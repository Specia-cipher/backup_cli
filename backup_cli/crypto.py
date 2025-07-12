# backup_cli/crypto.py

from cryptography.fernet import Fernet
import json
import base64
import os

KEYS_METADATA_FILE = os.path.expanduser("~/backup_storage/keys_metadata.json")

def generate_key():
    """Generate a new encryption key."""
    return Fernet.generate_key()

def encrypt_file(file_path, key, store_key=False, master_password=None):
    """Encrypt a file using the provided key."""
    fernet = Fernet(key)
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(file_path, 'wb') as f:
        f.write(encrypted)
    print(f"🔒 File encrypted: {file_path}")

    if store_key:
        save_encryption_key(file_path, key, master_password)

def decrypt_file(file_path, key):
    """Decrypt a file using the provided key."""
    fernet = Fernet(key)
    with open(file_path, 'rb') as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    with open(file_path, 'wb') as f:
        f.write(decrypted)
    print(f"🔓 File decrypted: {file_path}")

def save_encryption_key(file_path, key, master_password):
    """(Future) Save the encryption key, encrypted with a master password."""
    if not master_password:
        print("⚠️ Master password required to store encryption key.")
        return

    encrypted_key = Fernet(master_password.encode()).encrypt(key)
    metadata = load_keys_metadata()
    metadata[os.path.basename(file_path)] = {
        "encrypted_key": base64.urlsafe_b64encode(encrypted_key).decode()
    }
    with open(KEYS_METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"📦 Encryption key stored securely for {file_path}")

def load_keys_metadata():
    """Load existing keys metadata or return empty dict."""
    if os.path.exists(KEYS_METADATA_FILE):
        with open(KEYS_METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

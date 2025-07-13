import os
import sys
import shutil
import zipfile
import tarfile
import datetime
import tempfile
import json
import getpass
import logging
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.fernet import Fernet
import paramiko  # For SFTP support

# Config & Constants
BACKUP_STORAGE_DIR = Path.home() / 'backup_storage'
RECYCLE_BIN_DIR = BACKUP_STORAGE_DIR / 'recycle_bin'
AES_KEY_PATH = Path.home() / '.backup_cli_aes_key'
USERS_FILE = Path.home() / '.backup_cli_users.json'
LOG_FILE = Path.home() / 'backup_cli_audit.log'

SFTP_ENABLED = os.getenv('BACKUP_CLI_SFTP_ENABLED', 'false').lower() == 'true'
SFTP_HOST = os.getenv('BACKUP_CLI_SFTP_HOST', '')
SFTP_PORT = int(os.getenv('BACKUP_CLI_SFTP_PORT', '22'))
SFTP_USERNAME = os.getenv('BACKUP_CLI_SFTP_USERNAME', '')
SFTP_PASSWORD = os.getenv('BACKUP_CLI_SFTP_PASSWORD', '')
SFTP_REMOTE_DIR = os.getenv('BACKUP_CLI_SFTP_REMOTE_DIR', '/remote/backup/dir')

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# RBAC Roles
ROLES = {
    "admin": ["backup", "restore", "purge", "logs"],
    "operator": ["backup", "restore"],
    "auditor": ["logs"]
}

def log_action(action: str):
    logging.info(action)

# RBAC Authentication
def load_users():
    if USERS_FILE.exists():
        with USERS_FILE.open() as f:
            return json.load(f)
    else:
        return {}

def get_user_role(username):
    users = load_users()
    return users.get(username)

def require_permission(role, action):
    if action not in ROLES.get(role, []):
        print(f"❌ Permission Denied: Role '{role}' cannot perform '{action}'.")
        sys.exit(1)

# Encryption Key Management
def load_or_generate_key():
    if not AES_KEY_PATH.exists():
        print("🔑 No encryption key found.")
        choice = input("Generate a new AES encryption key? (Y/n): ").strip().lower()
        if choice in ['', 'y', 'yes']:
            key = os.urandom(32)
            AES_KEY_PATH.write_bytes(key)
            print(f"✅ New AES key generated and saved to {AES_KEY_PATH}")
            return key
        else:
            print("⚠️ Encryption will not be available without a key.")
            sys.exit(1)
    key = AES_KEY_PATH.read_bytes()
    if len(key) != 32:
        raise ValueError("Invalid AES key size. Expected 32 bytes.")
    return key

def create_backup_filename(base_name: str, ext: str) -> str:
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    return f"{base_name}_{timestamp}.{ext}"

def compress_folder(source_path: Path, dest_path: Path, method: str = 'zip'):
    if method == 'zip':
        with zipfile.ZipFile(dest_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_path):
                for file in files:
                    abs_file = Path(root) / file
                    rel_path = abs_file.relative_to(source_path)
                    zipf.write(abs_file, rel_path)
    elif method == 'tar.gz':
        with tarfile.open(dest_path, 'w:gz') as tar:
            tar.add(source_path, arcname=source_path.name)
    else:
        raise ValueError(f"Unsupported compression method: {method}")

def encrypt_file(in_path: Path, out_path: Path, key: bytes):
    data = in_path.read_bytes()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, data, None)
    out_path.write_bytes(nonce + encrypted)

def decrypt_file(in_path: Path, out_path: Path, key: bytes):
    data = in_path.read_bytes()
    nonce, encrypted = data[:12], data[12:]
    aesgcm = AESGCM(key)
    decrypted = aesgcm.decrypt(nonce, encrypted, None)
    out_path.write_bytes(decrypted)

def backup(source_path: str, compress_method='zip', encrypt=True) -> Path:
    source_path = Path(source_path).resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"Source path does not exist: {source_path}")

    BACKUP_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    base_name = source_path.name
    compressed_ext = 'zip' if compress_method == 'zip' else 'tar.gz'
    final_ext = compressed_ext + ('.enc' if encrypt else '')

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_compressed = Path(tmpdir) / create_backup_filename(base_name, compressed_ext)
        final_backup = BACKUP_STORAGE_DIR / create_backup_filename(base_name, final_ext)

        compress_folder(source_path, temp_compressed, method=compress_method)
        log_action(f"Compressed {source_path} -> {temp_compressed}")

        if encrypt:
            key = load_or_generate_key()
            encrypt_file(temp_compressed, final_backup, key)
            log_action(f"Encrypted {temp_compressed} -> {final_backup}")
        else:
            shutil.move(temp_compressed, final_backup)

        print(f"✅ Backup created at {final_backup}")
        log_action(f"Backup created: {final_backup}")

        if SFTP_ENABLED:
            sftp_upload(final_backup)

        return final_backup

def sftp_upload(local_path: Path):
    if not all([SFTP_HOST, SFTP_USERNAME, SFTP_PASSWORD]):
        print("❌ SFTP credentials not configured. Skipping upload.")
        return
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        remote_path = os.path.join(SFTP_REMOTE_DIR, local_path.name)
        sftp.put(str(local_path), remote_path)
        log_action(f"Uploaded {local_path} to SFTP {remote_path}")
        print(f"☁️ Uploaded {local_path} to cloud via SFTP")
        sftp.close()
    except Exception as e:
        print(f"❌ SFTP upload failed: {e}")
        log_action(f"SFTP upload failed: {e}")
    finally:
        transport.close()

# CLI Entry Point
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="🔒 Backup CLI with Encryption & RBAC")
    parser.add_argument('source', help="Source folder/file to back up")
    parser.add_argument('--compress', choices=['zip', 'tar.gz'], default='zip', help="Compression method")
    parser.add_argument('--no-encrypt', action='store_true', help="Disable encryption")
    parser.add_argument('--purge', type=int, help="Purge recycle bin files older than N days")
    parser.add_argument('--restore', metavar='FILENAME', help="Restore a file from recycle bin")
    parser.add_argument('--view-logs', action='store_true', help="View audit logs")
    args = parser.parse_args()

    username = getpass.getuser()
    role = get_user_role(username)
    if not role:
        print(f"❌ User '{username}' not found in RBAC database.")
        sys.exit(1)
    print(f"👤 User: {username} | Role: {role}")

    try:
        if args.purge:
            require_permission(role, 'purge')
            purge_recycle_bin(args.purge)
        elif args.restore:
            require_permission(role, 'restore')
            restore_from_recycle_bin(args.restore)
        elif args.view_logs:
            require_permission(role, 'logs')
            with open(LOG_FILE) as f:
                print(f.read())
        else:
            require_permission(role, 'backup')
            backup(args.source, compress_method=args.compress, encrypt=not args.no_encrypt)
    except Exception as e:
        print(f"❌ Operation failed: {e}")
        log_action(f"Operation failed: {e}")

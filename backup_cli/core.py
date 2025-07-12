# backup_cli/core.py

import os
import shutil
import datetime
from backup_cli.crypto import encrypt_file, decrypt_file, generate_key
import json

BACKUP_DIR = os.path.expanduser("~/backup_storage")
RECYCLE_BIN_DIR = os.path.join(BACKUP_DIR, "recycle_bin")
AUDIT_LOG_FILE = os.path.join(BACKUP_DIR, "audit.log")
RECYCLE_INDEX_FILE = os.path.join(RECYCLE_BIN_DIR, "recycle_index.json")


def init_storage():
    """Create the backup and recycle bin directories if they don't exist."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(RECYCLE_BIN_DIR, exist_ok=True)
    if not os.path.exists(RECYCLE_INDEX_FILE):
        with open(RECYCLE_INDEX_FILE, 'w') as f:
            json.dump({}, f)


# --- Backup ---
def create_backup(source, encrypt=False, compress=None):
    """
    Create a backup of the source directory.
    Supports optional encryption and compression.
    """
    init_storage()
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = os.path.basename(source.rstrip("/"))
    backup_name = f"{base_name}_{timestamp}"
    dest_path = os.path.join(BACKUP_DIR, backup_name)

    try:
        if compress == "zip":
            shutil.make_archive(dest_path, 'zip', source)
            dest_path += ".zip"
        elif compress == "tar.gz":
            shutil.make_archive(dest_path, 'gztar', source)
            dest_path += ".tar.gz"
        else:
            shutil.copytree(source, dest_path)

        if encrypt:
            key = generate_key()
            encrypt_file(dest_path, key)
            details = f"{backup_name} (encrypted=True, compressed={compress})"
        else:
            details = f"{backup_name} (encrypted=False, compressed={compress})"

        print(f"✅ Backup created at {dest_path}")
        log_action("add", details)

    except Exception as e:
        print(f"❌ Backup failed: {e}")
        log_action("error", f"Failed to backup {source}: {e}")


# --- List Backups ---
def list_backups():
    """List all backups in the backup directory."""
    init_storage()
    print("📦 Available backups:")
    for f in os.listdir(BACKUP_DIR):
        if f != "recycle_bin":
            print(f" - {f}")


# --- Restore ---
def restore_backup(backup_name, target_dir=None, key=None):
    """
    Restore a backup to a specified target directory.
    Decrypts and decompresses if necessary.
    """
    init_storage()
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    if not os.path.exists(backup_path):
        print(f"❌ Backup not found: {backup_name}")
        return

    if not target_dir:
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        target_dir = os.path.join(os.getcwd(), f"restored_{timestamp}")

    os.makedirs(target_dir, exist_ok=True)

    try:
        # Decrypt if needed
        if ".enc" in backup_name:
            if not key:
                raise ValueError("Encryption key required to decrypt this backup.")
            print("🔓 Decrypting backup...")
            decrypt_file(backup_path, key)

        # Decompress if needed
        if backup_name.endswith(".zip"):
            print("📦 Decompressing ZIP...")
            shutil.unpack_archive(backup_path, target_dir, 'zip')
        elif backup_name.endswith(".tar.gz"):
            print("📦 Decompressing TAR.GZ...")
            shutil.unpack_archive(backup_path, target_dir, 'gztar')
        else:
            # Copy uncompressed directory
            shutil.copytree(backup_path, target_dir, dirs_exist_ok=True)

        print(f"✅ Backup restored to {target_dir}")
        log_action("restore", f"{backup_name} -> {target_dir}")

    except Exception as e:
        print(f"❌ Restore failed: {e}")
        log_action("error", f"Failed to restore {backup_name}: {e}")


# --- Recycle Bin ---
def move_to_recycle_bin(backup_name):
    """Move a backup to the recycle bin instead of deleting it."""
    init_storage()
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    if not os.path.exists(backup_path):
        print(f"❌ Backup not found: {backup_name}")
        return

    dest_path = os.path.join(RECYCLE_BIN_DIR, backup_name)
    shutil.move(backup_path, dest_path)

    # Update recycle index
    recycle_index = load_recycle_index()
    recycle_index[backup_name] = {
        "deleted_at": datetime.datetime.now().isoformat()
    }
    save_recycle_index(recycle_index)

    print(f"🗑️ Moved to recycle bin: {backup_name}")
    log_action("recycle", backup_name)


def list_recycle_bin():
    """List backups in the recycle bin."""
    init_storage()
    recycle_index = load_recycle_index()
    if not recycle_index:
        print("🗑️ Recycle bin is empty.")
        return

    print("🗑️ Recycle Bin Contents:")
    for name, info in recycle_index.items():
        print(f" - {name} (deleted at {info['deleted_at']})")


def purge_recycle_bin(older_than_days=None):
    """Permanently delete backups from recycle bin."""
    init_storage()
    recycle_index = load_recycle_index()
    now = datetime.datetime.now()
    to_delete = []

    for name, info in recycle_index.items():
        deleted_at = datetime.datetime.fromisoformat(info['deleted_at'])
        if older_than_days:
            if (now - deleted_at).days >= older_than_days:
                to_delete.append(name)
        else:
            to_delete.append(name)  # purge all if no days specified

    for name in to_delete:
        path = os.path.join(RECYCLE_BIN_DIR, name)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        recycle_index.pop(name)
        print(f"❌ Permanently deleted: {name}")
        log_action("purge", name)

    save_recycle_index(recycle_index)


# --- JSON Helpers ---
def load_recycle_index():
    """Load recycle bin index."""
    if os.path.exists(RECYCLE_INDEX_FILE):
        with open(RECYCLE_INDEX_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_recycle_index(index):
    """Save recycle bin index."""
    with open(RECYCLE_INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=4)


# --- Audit Logging ---
def log_action(action, details):
    """Log an action to the audit log with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action.upper()}: {details}\n"
    with open(AUDIT_LOG_FILE, 'a') as log_file:
        log_file.write(entry)

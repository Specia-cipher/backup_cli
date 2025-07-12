# backup_cli/core.py
import os
import shutil
import datetime

BACKUP_DIR = os.path.expanduser("~/backup_storage")

def init_storage():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def create_backup(source, encrypt=False, compress=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = os.path.basename(source.rstrip("/"))
    backup_name = f"{base_name}_{timestamp}"
    dest_path = os.path.join(BACKUP_DIR, backup_name)

    if compress == "zip":
        shutil.make_archive(dest_path, 'zip', source)
        dest_path += ".zip"
    elif compress == "tar.gz":
        shutil.make_archive(dest_path, 'gztar', source)
        dest_path += ".tar.gz"
    else:
        shutil.copytree(source, dest_path)

    # TODO: Call encryption if encrypt=True

    print(f"✅ Backup created at {dest_path}")

def list_backups():
    print("📦 Available backups:")
    for f in os.listdir(BACKUP_DIR):
        print(f" - {f}")

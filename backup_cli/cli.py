#!/usr/bin/env python3
import os
import sys
import json
import boto3
import logging
import argparse
import paramiko
import zipfile
import tarfile
from io import BytesIO
from pathlib import Path
from getpass import getuser
from datetime import datetime
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

# Configuration - All configurable via ENV vars
class Config:
    # Core
    BACKUP_DIR = Path(os.getenv('BACKUP_DIR', str(Path.home() / 'backup_storage')))
    RECYCLE_BIN = BACKUP_DIR / 'recycle_bin'
    LOG_FILE = BACKUP_DIR / 'audit.log'
    USERS_FILE = Path(os.getenv('USERS_FILE', str(Path.home() / '.backup_cli/users.json')))
    KEY_FILE = Path(os.getenv('KEY_FILE', '/config/encryption.key'))
    
    # SFTP
    SFTP_ENABLED = os.getenv('SFTP_ENABLED', 'false').lower() == 'true'
    SFTP_HOST = os.getenv('SFTP_HOST', '')
    SFTP_PORT = int(os.getenv('SFTP_PORT', '22'))
    SFTP_USER = os.getenv('SFTP_USER', '')
    SFTP_PASS = os.getenv('SFTP_PASS', '')
    SFTP_REMOTE_DIR = os.getenv('SFTP_REMOTE_DIR', '/backups')

    # AWS S3
    S3_ENABLED = os.getenv('S3_ENABLED', 'false').lower() == 'true'
    S3_BUCKET = os.getenv('S3_BUCKET', '')
    S3_PREFIX = os.getenv('S3_PREFIX', 'backups/')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')

class BackupSentinel:
    def __init__(self):
        self._setup_dirs()
        self.user = getuser()
        self.role = self._load_user_role()
        self.logger = self._setup_logging()
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY
        ) if Config.S3_ENABLED else None

    # === Core Operations ===
    def backup(self, source_path: str, compress: str = 'zip', encrypt: bool = True):
        """Full backup pipeline with compression + encryption"""
        source = Path(source_path).resolve()
        if not source.exists():
            raise FileNotFoundError(f"Source not found: {source}")

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_name = f"{source.name}_{timestamp}.{compress}"
        backup_path = Config.BACKUP_DIR / backup_name

        # Compression
        self._compress(source, backup_path, compress)
        self.log(f"Compressed: {source} -> {backup_path}")

        # Encryption
        if encrypt:
            encrypted_path = self._encrypt_file(backup_path)
            backup_path.unlink()  # Remove unencrypted
            backup_path = encrypted_path

        # Remote sync
        self._sync_to_remote(backup_path)
        return backup_path

    def restore(self, backup_name: str, output_dir: str = None):
        """Restore pipeline with decryption"""
        backup_path = Config.BACKUP_DIR / backup_name
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_name}")

        output_path = Path(output_dir) if output_dir else Config.BACKUP_DIR / 'restored'
        output_path.mkdir(exist_ok=True)

        # Handle encrypted files
        if backup_name.endswith('.enc'):
            decrypted_path = self._decrypt_file(backup_path)
            backup_path = decrypted_path

        # Decompress
        self._decompress(backup_path, output_path)
        self.log(f"Restored: {backup_path} -> {output_path}")
        return output_path

    # === Storage Integrations ===
    def _sync_to_remote(self, local_path: Path):
        """Push to all configured remote targets"""
        if Config.SFTP_ENABLED:
            self._sftp_upload(local_path)
        if Config.S3_ENABLED:
            self._s3_upload(local_path)

    def _s3_upload(self, local_path: Path):
        """Upload to AWS S3"""
        try:
            s3_key = f"{Config.S3_PREFIX}{local_path.name}"
            self.s3.upload_file(
                str(local_path),
                Config.S3_BUCKET,
                s3_key
            )
            self.log(f"Uploaded to S3: s3://{Config.S3_BUCKET}/{s3_key}")
        except ClientError as e:
            self.log(f"S3 upload failed: {e}", level='error')

    # === Security ===
    def _encrypt_file(self, input_path: Path) -> Path:
        """Encrypt file with Fernet"""
        key = self._get_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(input_path.read_bytes())
        output_path = input_path.with_suffix(input_path.suffix + '.enc')
        output_path.write_bytes(encrypted)
        return output_path

    def _decrypt_file(self, input_path: Path) -> Path:
        """Decrypt Fernet-encrypted file"""
        key = self._get_key()
        cipher = Fernet(key)
        decrypted = cipher.decrypt(input_path.read_bytes())
        output_path = input_path.with_suffix('')  # Remove .enc
        output_path.write_bytes(decrypted)
        return output_path

    # === Utility Methods ===
    def _compress(self, source: Path, dest: Path, method: str):
        """Compress using zip or tar.gz"""
        if method == 'zip':
            with zipfile.ZipFile(dest, 'w') as zipf:
                for file in source.rglob('*'):
                    zipf.write(file, file.relative_to(source))
        else:  # tar.gz
            with tarfile.open(dest, 'w:gz') as tar:
                tar.add(source, arcname=source.name)

    def _decompress(self, archive: Path, output_dir: Path):
        """Extract compressed archives"""
        if archive.suffix == '.zip':
            with zipfile.ZipFile(archive) as zipf:
                zipf.extractall(output_dir)
        else:  # .tar.gz
            with tarfile.open(archive) as tar:
                tar.extractall(output_dir)

    def _sftp_upload(self, local_path: Path):
        """Upload to SFTP server"""
        transport = paramiko.Transport((Config.SFTP_HOST, Config.SFTP_PORT))
        transport.connect(username=Config.SFTP_USER, password=Config.SFTP_PASS)
        try:
            sftp = paramiko.SFTPClient.from_transport(transport)
            remote_path = f"{Config.SFTP_REMOTE_DIR}/{local_path.name}"
            sftp.put(str(local_path), remote_path)
            self.log(f"Uploaded to SFTP: {remote_path}")
        finally:
            transport.close()

    def _get_key(self) -> bytes:
        """Get or generate encryption key"""
        if not Config.KEY_FILE.exists():
            key = Fernet.generate_key()
            Config.KEY_FILE.write_bytes(key)
        return Config.KEY_FILE.read_bytes()

    def _load_user_role(self) -> str:
        """Load RBAC role with auto-init"""
        if not Config.USERS_FILE.exists():
            Config.USERS_FILE.write_text(json.dumps({self.user: "admin"}))
        users = json.loads(Config.USERS_FILE.read_text())
        return users.get(self.user, "operator")

    def _setup_dirs(self):
        """Ensure required directories exist"""
        Config.BACKUP_DIR.mkdir(exist_ok=True)
        Config.RECYCLE_BIN.mkdir(exist_ok=True)

    def _setup_logging(self):
        """Configure audit logging"""
        logging.basicConfig(
            filename=Config.LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('backup_sentinel')

    def log(self, message: str, level: str = 'info'):
        """Unified logging"""
        getattr(self.logger, level)(message)
        print(f"[{level.upper()}] {message}")

# CLI Interface
def main():
    parser = argparse.ArgumentParser(description="🔐 Backup Sentinel CLI")
    parser.add_argument('source', nargs='?', help="Path to backup")
    parser.add_argument('--compress', choices=['zip', 'tar.gz'], default='zip')
    parser.add_argument('--no-encrypt', action='store_true')
    parser.add_argument('--restore', metavar='BACKUP_NAME', help="Restore a backup")
    parser.add_argument('--output-dir', help="Restoration output directory")
    parser.add_argument('--list', action='store_true', help="List available backups")
    
    args = parser.parse_args()
    sentinel = BackupSentinel()

    try:
        if args.list:
            backups = [f.name for f in Config.BACKUP_DIR.glob('*')]
            print("Available backups:\n" + "\n".join(backups))
        elif args.restore:
            restored_path = sentinel.restore(args.restore, args.output_dir)
            print(f"✅ Restored to: {restored_path}")
        elif args.source:
            backup_path = sentinel.backup(
                args.source,
                compress=args.compress,
                encrypt=not args.no_encrypt
            )
            print(f"✅ Backup created: {backup_path}")
        else:
            parser.print_help()
    except Exception as e:
        sentinel.log(f"Operation failed: {e}", 'error')
        sys.exit(1)

if __name__ == "__main__":
    main()

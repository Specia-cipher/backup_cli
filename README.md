🛡️ Backup Sentinel CLI  
A modular, enterprise-ready CLI for secure, encrypted, and versioned backups.  
Built for sysadmins, developers, and organizations that care about data integrity, disaster recovery, and operational excellence.  

"Surgical precision for your backups. Anywhere. Anytime."  

📑 Table of Contents  
🚀 Features  
📦 Installation  
📘 Usage Examples  
🐳 Docker Support  
🗑️ Recycle Bin  
📜 Audit Logs  
👥 RBAC Authentication  
☁️ Cloud Storage (SFTP/S3)  
👨‍💻 About the Author  
📜 License  

🚀 Features  
✅ AES-256 Encryption – Military-grade encryption for backups  
✅ Role-Based Access Control (RBAC) – user-level permissions  
✅ Versioned Backups – Automatic timestamped versions  
✅ Cross-Platform – Linux/macOS/Windows via Docker  
✅ Cloud Sync – Simultaneous SFTP & AWS S3 uploads  

📦 Installation  
```bash
# Local development  
git clone https://github.com/Specia-cipher/backup_cli.git  
cd backup_cli  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

# Production deployment  
docker build -t backup-sentinel .
📘 Usage Examples
Create Encrypted Backup

bash
python3 -m backup_cli.cli ~/important_files --compress zip  
# Output: ✅ Backup created at /backups/important_files_20250715-142310.zip.enc  
Restore from Backup

bash
python3 -m backup_cli.cli --restore important_files_20250715-142310.zip.enc  
# Output: ✅ Restored to /restored/important_files_20250715-142856  
🐳 Docker Support

bash
# Minimal deployment  
docker run --rm -v /host/data:/data -v /host/backups:/backups backup-sentinel /data  

# Full production example:  
docker run -d \  
  -v /mnt/backups:/backups \  
  -v /mnt/data:/data \  
  -e S3_ENABLED=true \  
  -e SFTP_HOST=backup.example.com \  
  --name backup-sentinel \  
  backup-sentinel
☁️ Cloud Storage
AWS S3 Configuration

bash
export S3_BUCKET="your-backup-bucket"  
export AWS_ACCESS_KEY_ID="AKIA..."  
export AWS_SECRET_ACCESS_KEY="..."  
SFTP Configuration

bash
export SFTP_HOST="backup.example.com"  
export SFTP_USER="backup_user"  
export SFTP_PASS="..."  
👥 RBAC Authentication

json
// .backup_cli_users.json  
{  
  "admin": "admin",  
  "ops_team": "operator"  
}
👨‍💻 About the Author
Sanni Babatunde Idris

GitHub: github.com/Specia-cipher

LinkedIn: linkedin.com/in/sanni-idris

📜 License
MIT License - See LICENSE.md for details.



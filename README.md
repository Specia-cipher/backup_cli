# 🛡️ Backup Sentinel CLI

A modular, enterprise-ready CLI for **secure, encrypted, and versioned backups**.  
Built for sysadmins, developers, and organizations that care about **data integrity**, **disaster recovery**, and **operational excellence**.

> **"Surgical precision for your backups. Anywhere. Anytime."**

---

## 📑 Table of Contents

- [🚀 Features](#-features)  
- [📦 Installation](#-installation)  
- [📘 Usage Examples](#-usage-examples)  
  - [Create Backup](#create-backup)  
  - [Restore Backup](#restore-backup)  
  - [Recycle Bin](#recycle-bin)  
  - [Audit Logs](#audit-logs)  
  - [RBAC Authentication](#rbac-authentication)  
  - [SFTP Upload](#sftp-upload)  
- [🐳 Docker Support](#-docker-support)  
- [🗺 Roadmap](#-roadmap)  
- [👨‍💻 About the Author](#-about-the-author)  
- [📜 License](#-license)  

---

## 🚀 Features

✅ **AES-256 Encryption** – Strong encryption for secure backups.  
✅ **Role-Based Access Control (RBAC)** – Fine-grained permissions for multi-user environments.  
✅ **Versioned Backups** – Timestamped and safely stored.  
✅ **Recycle Bin** – Soft delete with restore & purge options.  
✅ **Audit Logging** – Tracks all operations for accountability.  
✅ **SFTP Support** – Upload backups to remote servers securely.  
✅ **Compression** – Supports `.zip` and `.tar.gz` archives.  
✅ **Clean CLI UX** – Clear output and helpful prompts.  
✅ **Docker Support** – Containerized deployments for modern infrastructures.  

---

## 📦 Installation

```bash
git clone https://github.com/Specia-cipher/backup_cli.git
cd backup_cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


---

📘 Usage Examples

🔥 Create Backup

python3 -m backup_cli.cli /home/userland/testdata --compress zip

✅ Output:

👤 User: userland | Role: admin
✅ Backup created at /home/userland/backup_storage/testdata_20250712-163131.zip.enc


---

🔓 Restore Backup

python3 -m backup_cli.cli --restore testdata_20250712-163131.zip.enc

✅ Output:

👤 User: userland | Role: operator
🔓 Decrypting backup...
📦 Decompressing ZIP...
✅ Backup restored to /home/userland/restored_20250712-171045


---

🗑️ Recycle Bin

Move backup to recycle bin:

python3 -m backup_cli.cli --purge 30

✅ Output:

🗑️ Moved to recycle bin: testdata_20250712-163131.zip.enc
🧹 Purged files older than 30 days


---

📜 Audit Logs

python3 -m backup_cli.cli --view-logs

✅ Output:

2025-07-12 16:31:31 - INFO - Backup created: testdata_20250712-163131.zip.enc
2025-07-12 16:35:12 - INFO - Restored testdata_20250712-163131.zip.enc


---

👥 RBAC Authentication

Each user must exist in .backup_cli_users.json:

{
  "adminuser": "admin",
  "operatoruser": "operator",
  "auditoruser": "auditor"
}


---

☁️ SFTP Upload

Enable by setting environment variables:

export BACKUP_CLI_SFTP_ENABLED=true
export BACKUP_CLI_SFTP_HOST=sftp.example.com
export BACKUP_CLI_SFTP_PORT=22
export BACKUP_CLI_SFTP_USERNAME=youruser
export BACKUP_CLI_SFTP_PASSWORD=yourpass
export BACKUP_CLI_SFTP_REMOTE_DIR=/remote/backup/dir

Backups are automatically uploaded after creation:

☁️ Uploaded /home/userland/backup_storage/testdata_20250712-163131.zip.enc to cloud via SFTP


---

🐳 Docker Support

Build and run:

docker build -t backup-sentinel .
docker run --rm backup-sentinel --help


---

🗺 Roadmap

✅ Phase 1: Core Features Complete
🚀 Phase 2:

[x] Role-Based Access Control (RBAC)

[x] SFTP Upload Support

[ ] Cloud Storage Integrations (AWS S3, GCP, Dropbox)

[ ] Scheduler (Cron, Systemd support)

[ ] Healthcheck API for Docker/K8s



---

👨‍💻 About the Author

🔖 Built with ❤️ by Sanni Babatunde Idris
GitHub: github.com/Specia-cipher
LinkedIn: linkedin.com/in/sanni-idris-89917a262


---

📜 License

MIT – Free as in freedom. Protect your data.

---

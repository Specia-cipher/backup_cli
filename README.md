# 🛡️ Backup Sentinel CLI

A modular, enterprise-ready CLI for **secure, encrypted, and versioned backups**.  
Built for developers, sysadmins, and organizations that care about **data integrity**, **disaster recovery**, and **operational excellence**.

> **"Surgical precision for your backups. Anywhere. Anytime."**  

---

## 🚀 Current Features (Phase 1)

✅ **AES-256 Encryption** – Strong symmetric encryption for all backups.  
✅ **Versioned Backups** – Each backup is timestamped and safely stored.  
✅ **Compression Support** – Supports ZIP and TAR.GZ for optimized storage.  
✅ **Recycle Bin** – Safe delete with restore/purge capabilities.  
✅ **Audit Logging** – Forensic-grade logs of all operations.  
✅ **Polished CLI UX** – Clean interface with rich ASCII branding.  
✅ **Tested Environments** – Kali Linux (UserLAnd), Termux, and BackBox VM.

---

## 🔥 Phase 2 (In Progress)

We are engineering Backup Sentinel CLI for **enterprise-grade environments**:  

🗄️ **Cloud Sync** – Seamless integration with AWS S3, Google Cloud Storage, Dropbox, and SFTP servers.  
⏳ **Scheduled Backups** – Cron/Systemd support for automated routines.  
👥 **Multi-User RBAC** – Role-based access control for team environments.  
⚙️ **Configurable Storage** – Centralized config file with environment overrides.  
🌐 **Healthcheck API** – Lightweight HTTP endpoint for Docker/K8s readiness checks.  

---

## 🐳 Docker Support

A Dockerfile and docker-compose.yml are included for containerized deployments:

docker build -t backup-sentinel . docker run --rm backup-sentinel --help

Why Docker?  
✅ Isolated, reproducible environments  
✅ Easy cloud-native deployments  
✅ Portability across dev/test/prod stages  

---

## 👨‍💻 About the Author

🔖 Built with ❤️ and surgical precision by **Sanni Babatunde Idris**  
GitHub: [github.com/Specia-cipher](https://github.com/Specia-cipher)  
LinkedIn: [linkedin.com/in/sanni-idris-89917a262](https://linkedin.com/in/sanni-idris-89917a262)

---

## 🚧 Status
**Phase 1: Complete 🎯**  
**Phase 2: In Progress 🚀 (Cloud Sync → Scheduler → RBAC → API)**

git clone https://github.com/Specia-cipher/backup_cli.git cd backup_cli python3 -m backup_cli.cli --help

---

## 📜 License
MIT – Free as in freedom. Protect your data.

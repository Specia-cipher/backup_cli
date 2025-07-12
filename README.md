🛡️ Backup Sentinel CLI – Luxury or Nothing Edition

"Life is narrow and steep, far and near." – Special Agent Sanni Babatunde Idris

Backup Sentinel CLI is a cross-platform, encrypted backup utility designed for versioned local snapshots, with a roadmap to cloud-synced, enterprise-grade deployments. Built in a pocket-sized Kali Linux lab (via UserLAnd), it is secure, efficient, and battle-ready.

This isn’t just a tool. It’s a sentinel watching over your data.


---

🚀 Current Status: Phase 1 Complete

🌟 Mobile Lab MVP ✅ Versioned backups with timestamped snapshots
✅ AES-256 encryption for all sensitive data
✅ Compression support (ZIP, TAR.GZ)
✅ Recycle bin for safe delete/restore operations
✅ Audit logs for every action (forensic-friendly)
✅ Clean CLI UX with ASCII branding and progress feedback


---

🛡️ Why Backup Sentinel CLI?

> "The warrior who controls himself is mightier than the one who controls armies." – Sun Tzu



Backup Sentinel CLI controls chaos with:
✔️ Portable local backups
✔️ Military-grade encryption
✔️ Recycle bin for accidental deletes
✔️ A clear path to enterprise-scale ops


---

📦 Features

Feature	Status

🕰️ Timestamped versioning	✅ Complete
🔒 AES-256 encryption	✅ Complete
💜 Compression (zip, tar.gz)	✅ Complete
🗑️ Recycle bin (delete/restore)	✅ Complete
📖 Audit logging	✅ Complete
🔍 Professional CLI UX	✅ Complete
☁️ Cloud sync (S3, Dropbox, GCP)	🔜 Phase 2
🕒 Scheduled backups (cron support)	🔜 Phase 2
🐳 Dockerized deployment	🔜 Phase 2
👥 Multi-user RBAC	🔜 Phase 2
💻 Daemon/service mode	🔜 Phase 2



---

🗓️ Roadmap

Phase	ETA

🛡️ Phase 1: Mobile Lab MVP	✅ July 2025
🌐 Phase 2: Enterprise Edition	🔜 Aug 2025



---

💻 Quickstart

🛠️ Install

git clone https://github.com/Specia-cipher/backup_sentinel_cli.git
cd backup_sentinel_cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


---

📖 Usage Examples

📁 Create Backup

python3 -m backup_cli.cli add ~/Documents --encrypt --compress zip

📦 List Backups

python3 -m backup_cli.cli list

🔄 Restore Backup

python3 -m backup_cli.cli restore Documents_20250712-163131.zip --key <encryption_key>

🗑️ Delete Backup (Recycle Bin)

python3 -m backup_cli.cli delete Documents_20250712-163131.zip

♻️ Restore from Recycle Bin

python3 -m backup_cli.cli recycle restore Documents_20250712-163131.zip

🧹 Purge Old Backups

python3 -m backup_cli.cli purge --older-than 30

📜 View Audit Logs

python3 -m backup_cli.cli logs


---

🗡️ Phase 2 – Enterprise Edition (Coming Soon)

☁️ Cloud Sync (AWS S3, GCP, Dropbox)

🕒 Scheduled Backups (cron/systemd)

🐳 Dockerized Deployment

👥 Role-Based Access Control (RBAC)

💻 Service Mode (background daemon)


"A sentinel is never idle."


---

👨‍💻 Author Watermark

Sanni Babatunde Idris – (Specia-cipher)
GitHub:  github.com/Specia-cipher
LinkedIn: linkedin.com/in/sanni-idris
Email:   sannifreelancer6779@gmail.com

🕵️️ Built with surgical precision in a Kali mobile lab.


---

📜 License

MIT – Free to use, modify, and share.


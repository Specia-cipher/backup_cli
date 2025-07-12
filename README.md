# 🗄️ Backup CLI Supreme – Luxury or Nothing Edition

> *"Life is narrow and steep, far and near." – Special Agent Idris*

A feature-rich backup CLI tool crafted in Termux and now running stronger than ever in a **pocket-sized Kali Linux lab (via UserLAnd)**. Designed for encrypted, versioned local backups and scalable to cloud-synced, Dockerized deployments.

---

## 🚀 Current Status: MVP Live
✅ **Versioned backups** with timestamped snapshots  
✅ **Compression support** (ZIP, TAR.GZ)  
✅ **Beautiful CLI UX** (progress bars, ASCII branding)  
✅ **Fully functional in Termux and Kali (UserLAnd)** – a true mobile lab  
🔜 **Next:** Encryption, purge logic, and audit logs

---

## 📦 Core Features (Phase 1)
- 🔒 AES-256 encryption (**coming up**)
- 📦 Versioned backups with timestamps
- 🗜️ Compression support (`zip`, `tar.gz`)
- 🔄 Selective restore (`--restore <date>`)
- 🧹 Purge old backups (`--purge --older-than 30d`)
- 📖 JSON-based backup index
- 🖋️ Clean CLI UX with Click & Rich

---

## 💻 Quickstart

### 🛠 Install
```bash
git clone https://github.com/Specia-cipher/backup_cli.git
cd backup_cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

📖 Usage Examples

📁 Create Backup

python3 -m backup_cli.cli add ~/Documents --compress zip

📦 List Backups

python3 -m backup_cli.cli list

🔄 Restore Backup

python3 -m backup_cli.cli restore ~/Documents --date 2025-07-12

🧹 Purge Old Backups

python3 -m backup_cli.cli purge --older-than 30d


---

🗡️ Roadmap

🥇 Phase 1 – Termux/Kali Pocket Lab MVP

Task	Status

📁 Project Scaffold	✅ Complete
🗜️ Compression Support	✅ Complete
📦 Backup & Restore Core	✅ Complete
🔒 AES Encryption Module	🔜 Pending
🧹 Purge Command	🔜 Pending
🖋️ CLI UX Polish	🔜 Pending
📖 CLI Help & Docs	🔜 Pending



---

🏯 Phase 2 – BackBox/WSL Upgrade (Enterprise Edition)

☁️ Cloud Sync (AWS S3, GCP, Dropbox)

📅 Scheduled Backups

👥 Multi-User Support (RBAC)

🐳 Dockerization (Dockerfile + docker-compose)

🖥️ Service Mode (background daemon)



---

🥷 Sun Tzu Principle Applied

"The warrior who controls himself is mightier than the one who controls armies."
This CLI controls chaos with elegance and speed.


---

👨‍💻 Author

Sanni Babatunde Idris – Special Agent
GitHub: Specia-cipher
LinkedIn: Sanni Idris
Gmail: sannifreelancer6779@gmail.com

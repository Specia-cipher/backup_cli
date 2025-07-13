FROM python:3.11-slim

# Metadata
LABEL maintainer="Sanni Babatunde Idris"
LABEL description="Backup Sentinel CLI - Phase 2 (With Cloud Support)"

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BACKUP_DIR=/backups \
    USERS_FILE=/config/users.json \
    KEY_FILE=/config/encryption.key

# Install dependencies (including new cloud packages)
RUN pip install --no-cache-dir \
    cryptography \
    paramiko \
    boto3 \
    && mkdir -p /backups /config

WORKDIR /app

# Copy only necessary files
COPY backup_cli/ ./backup_cli/
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Entrypoint
ENTRYPOINT ["python", "-m", "backup_cli.cli"]


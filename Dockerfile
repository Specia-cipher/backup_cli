# Use official Python base image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Sanni Babatunde Idris <sannifreelancer6779@gmail.com>"
LABEL description="Backup Sentinel CLI – Phase 1 (Encrypted backups, Recycle bin, Audit logging)"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY backup_cli /app/backup_cli
COPY README.md /app/
COPY . /app/

# Set entrypoint for CLI
ENTRYPOINT ["python3", "-m", "backup_cli.cli"]

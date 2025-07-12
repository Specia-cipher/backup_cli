# backup_cli/cli.py

import click
import os
import shutil
from backup_cli import core

@click.group()
def cli():
    """🗄️ Backup CLI Supreme – Luxury or Nothing Edition"""
    click.echo("🚀 Backup CLI Supreme – Luxury or Nothing Edition\n")

# --- Add Backup ---
@cli.command()
@click.argument('source')
@click.option('--encrypt', is_flag=True, help="Enable AES-256 encryption.")
@click.option('--compress', type=click.Choice(['zip', 'tar.gz']), help="Compress backup.")
def add(source, encrypt, compress):
    """Add a directory/file to the backup archive."""
    core.create_backup(source, encrypt, compress)

# --- List Backups ---
@cli.command()
def list():
    """List all backups."""
    core.list_backups()

# --- Restore Backup ---
@cli.command()
@click.argument('name')
@click.option('--target', help="Target directory to restore into.")
@click.option('--key', help="Encryption key if backup is encrypted.")
def restore(name, target, key):
    """Restore a backup by name."""
    core.restore_backup(name, target, key)

# --- Move to Recycle Bin ---
@cli.command()
@click.argument('name')
def delete(name):
    """Move a backup to the recycle bin instead of deleting permanently."""
    core.move_to_recycle_bin(name)

# --- Recycle Bin Group ---
@cli.group()
def recycle():
    """Manage the recycle bin (list, restore, purge)."""
    pass

@recycle.command('list')
def recycle_list():
    """List backups in the recycle bin."""
    core.list_recycle_bin()

@recycle.command('restore')
@click.argument('name')
def recycle_restore(name):
    """Restore a backup from recycle bin to backups directory."""
    recycle_bin_path = os.path.join(core.RECYCLE_BIN_DIR, name)
    target_path = os.path.join(core.BACKUP_DIR, name)

    if not os.path.exists(recycle_bin_path):
        click.echo(f"❌ Backup not found in recycle bin: {name}")
        return

    try:
        shutil.move(recycle_bin_path, target_path)
        recycle_index = core.load_recycle_index()
        recycle_index.pop(name, None)
        core.save_recycle_index(recycle_index)
        click.echo(f"✅ Restored from recycle bin: {name}")
        core.log_action("restore-recycle", name)
    except Exception as e:
        click.echo(f"❌ Failed to restore: {e}")

@recycle.command('purge')
@click.option('--older-than', type=int, help="Purge recycle bin backups older than N days.")
def recycle_purge(older_than):
    """Permanently delete recycle bin backups."""
    core.purge_recycle_bin(older_than)

# --- Audit Logs ---
@cli.command()
def logs():
    """Show last 10 audit log entries."""
    log_path = core.AUDIT_LOG_FILE
    if not os.path.exists(log_path):
        click.echo("📜 No audit log found.")
        return

    with open(log_path, 'r') as f:
        lines = f.readlines()[-10:]

    if not lines:
        click.echo("📜 Audit log is empty.")
        return

    click.echo("📜 Last 10 Audit Log Entries:")
    for line in lines:
        click.echo(f" - {line.strip()}")

# --- Purge Old Backups ---
@cli.command()
@click.option('--older-than', type=int, help="Move backups older than N days to recycle bin.")
def purge(older_than):
    """Move old backups to recycle bin."""
    if older_than is None:
        click.echo("❌ Please specify --older-than <days>")
        return

    from datetime import datetime
    now = datetime.now()

    for f in os.listdir(core.BACKUP_DIR):
        if f == "recycle_bin":
            continue  # Skip recycle bin directory

        backup_path = os.path.join(core.BACKUP_DIR, f)
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_path))
        if (now - mtime).days >= older_than:
            core.move_to_recycle_bin(f)

if __name__ == '__main__':
    cli()

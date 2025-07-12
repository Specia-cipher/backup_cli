# backup_cli/cli.py

import click
from backup_cli import core

@click.group()
def cli():
    """🗄️ Backup CLI Supreme – Luxury or Nothing Edition"""
    pass

@cli.command()
@click.argument('source')
@click.option('--encrypt', is_flag=True, help="Enable AES-256 encryption.")
@click.option('--compress', type=click.Choice(['zip', 'tar.gz']), help="Compress backup.")
def add(source, encrypt, compress):
    """Add a directory/file to the backup archive."""
    core.init_storage()
    core.create_backup(source, encrypt, compress)

@cli.command()
def list():
    """List all backups."""
    core.init_storage()
    core.list_backups()

@cli.command()
def logs():
    """Show last 10 audit log entries."""
    click.echo("📜 Audit logs coming soon...")

@cli.command()
@click.argument('name')
def restore(name):
    """Restore a backup."""
    click.echo(f"🔄 Restoring backup: {name}")

@cli.command()
@click.option('--older-than', type=int, help="Purge backups older than N days.")
def purge(older_than):
    """Purge old backups."""
    click.echo(f"🧹 Purging backups older than {older_than} days...")

if __name__ == '__main__':
    cli()

from pathlib import Path
import click
import os

from database import db_url


@click.group()
def cli():
    pass

@cli.command()
@click.option('--message', '-m', default='automigration')
def makemigrations(message: str) -> None:
    os.system(f'alembic revision --autogenerate -m "{message}"')


@cli.command()
def migrate() -> None:
    os.system('alembic upgrade head')


@cli.command()
@click.option('--message', '-m', default='automigration')
def ezmigrate(message: str) -> None:
    """Make migrations and migrate in one command."""
    makemigrations(message)
    migrate()


@cli.command()
def update_alembic_db_url():
    """Update the database url in alembic.ini from your database.py file."""
    alembic_ini = Path('alembic.ini')
    alembic_ini_lines = alembic_ini.read_text().splitlines()
    sqlalchemy_line_index = [index for index, line in enumerate(alembic_ini_lines) if line.startswith('sqlalchemy.url')][0]
    alembic_ini_lines[sqlalchemy_line_index] = f'sqlalchemy.url = {db_url}'.replace('\\', '/')
    alembic_ini.write_text('\n'.join(alembic_ini_lines))


if __name__ == '__main__':
    cli()
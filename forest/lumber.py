import click
import secrets

from flask import current_app
from werkzeug.security import generate_password_hash

from forest.db import get_db


def create_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def load_data():
    db = get_db()

    with current_app.open_resource('data.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('create-db')
def create_db_task():
    """Clear the existing data and create new tables"""
    create_db()
    click.echo('Created the database')


@click.command('load-data')
def load_data_task():
    """Populate the database with default data"""
    load_data()
    click.echo('Populated the database')


@click.command('generate-key')
def generate_key_task():
    click.echo(secrets.token_hex())


@click.command('hash-password')
@click.argument('password')
def hash_password_task(password):
    click.echo(generate_password_hash(password, method='pbkdf2:sha512'))


def register(app):
    app.cli.add_command(create_db_task)
    app.cli.add_command(load_data_task)
    app.cli.add_command(generate_key_task)
    app.cli.add_command(hash_password_task)

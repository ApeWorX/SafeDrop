from pathlib import Path

import click
from ape.cli import ape_cli_context
from ape.utils import to_int

from ._lib import DB


def db_option():
    return click.option("--db", type=Path, callback=lambda _0, _1, val: DB(path=val))


@click.group()
def cli():
    """
    Merkle tools
    """


@cli.command()
@ape_cli_context()
@db_option()
def purge(ape, db):
    """Delete the DB"""
    db.purge()
    ape.logger.success("DB purged.")


def _claims_callack(ctx, param, value) -> dict[str, int]:
    return _claim_list_to_dict(value)


def _claim_list_to_dict(claim_list: list[str]) -> dict[str, int]:
    # Convert a list of strings like `<address>=<amount>` to
    # a dictionary with address as the key and the amount
    # as the value.
    values = list(claim_list or [])
    result: dict[str, int] = {}
    for value in values:
        address, claim_amount = value.split("=")
        address = address.strip()
        result[address.strip()] = int(claim_amount.strip())

    return result


@cli.command()
@ape_cli_context()
@db_option()
@click.argument("claims", metavar="ADDRESS=CLAIM_AMOUNT", nargs=-1, callback=_claims_callack)
def add(ape, db, claims):
    """Add one or more claim(s) to the DB"""
    db.add(*claims)
    ape.logger.success("Claims added.")


def _import_file_callback(ctx, param, value):
    lines = Path(value).read_text().splitlines()
    return _claim_list_to_dict(lines)


# NOTE: import is a builtin key-word.
@cli.command(name="import")
@ape_cli_context()
@db_option()
@click.argument("claims", type=click.Path(exists=True), callback=_import_file_callback)
def import_from_file(ape, db, claims):
    """
    Import addresses from a file
    """
    db.add(*claims)
    ape.logger.success("Claims added.")


@cli.command()
@ape_cli_context()
@db_option()
@click.argument("addresses", metavar="ADDRESS", nargs=-1)
def remove(ape, db, addresses):
    """
    Remove one or more claim(s) from the DB
    """
    db.remove(*addresses)
    ape.logger.success("Claims removed.")


@cli.command()
@db_option()
@click.argument("address")
def get(db, address):
    """Get the value stored"""
    if result := db.get(address):
        # Assumes they were expecting it to exist
        # (different than 'check')
        click.echo(f"{to_int(result)}")

    else:
        click.abort("Address '{address}' not  found")


@cli.command()
@db_option()
@click.argument("address")
def check(db, address):
    """Check if an address is in the tree"""
    result = db.get(address)
    suffix = f"is present (result={to_int(result)})" if result else "is NOT present"
    click.echo(f"Address '{address}' {suffix}")


@cli.command()
@db_option()
@click.argument("address")
def proove(db, address):
    """
    Get a merkle proof
    """
    result = db.proove(address)
    click.echo("\n".join(result))


@cli.command()
@db_option()
def root(db):
    """
    Get the merkel root
    """
    click.echo(db.root)

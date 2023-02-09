#!/usr/bin/env python3
"""
NAME
    master -- Generates deterministic passwords for services

USAGE
    master [ls]         Lists all stored services
    master get NAME     Gets the password for service NAME
    master rm NAME      Removes service NAME from the stored list
    master version      Shows the version
    master help         Shows this help
"""
import os
import sys
import click
import hashlib
import base64
import getpass
import re

from . import VERSION
from .master import Master


MASTER_LIST = os.environ.get(
    "MASTER_LIST",
    os.path.expanduser("~/.config/master/list.txt")
)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand:
        pass
    else:
        ls()


@cli.command()
@click.argument("service", type=str)
@click.option("--chunks", type=int, default=Master.CHUNKS,
    help=f"The number of chunks (default: {Master.CHUNKS})"
)
@click.option("--counter", type=int, default=0,
    help="The password counter (default: 0)"
)
def get(service: str, chunks: int, counter: int):
    """Gets the deterministic password for SERVICE."""

    master = Master(MASTER_LIST)
    services = master.load()
    services.add(service)
    master.save(services)

    password = master.generate(service, chunks, counter)
    print(password)


@cli.command()
def ls():
    """Lists all stored services."""
    master = Master(MASTER_LIST)
    for service in master.load():
        print(service)


@cli.command()
def version():
    """Shows the version."""
    print(f"v{VERSION}")


@cli.command()
@click.argument("service", type=str)
def rm(service: str):
    """Removes SERVICE from the stored list."""
    master = Master(MASTER_LIST)
    services = master.load()
    services.discard(service)
    master.save(services)


if __name__ == "__main__":
    cli()

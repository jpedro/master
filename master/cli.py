#!/usr/bin/env python3
"""
NAME
    master -- Generates deterministic passwords for services

USAGE
    master                  Lists all stored services
    master NAME             Gets the password for service NAME
    master -r, --rm NAME    Removes service NAME from the stored list
    master -v, --version    Shows the version
    master -h, --help       Shows this help
"""
import os
import sys
import hashlib
import base64
import getpass
import re

from . import VERSION
from .master import Master


USER_HOME = os.path.expanduser("~")
MASTER_LIST = os.environ.get("MASTER_LIST", f"{USER_HOME}/.config/master/list.txt")


class Cli:

    def get(self, service: str, chunks: int = Master.CHUNKS, counter: int = 0):
        """Gets the deterministic password for SERVICE."""

        master = Master(MASTER_LIST)
        services = master.load()
        services.add(service)
        master.save(services)

        password = master.generate(service, chunks, counter)
        print(password)


    def ls(self):
        """Lists all stored services."""
        master = Master(MASTER_LIST)
        for service in master.load():
            print(service)


    def version(self):
        """Prints the version."""
        print(f"v{VERSION}")


    def remove(self, service: str):
        """Removes SERVICE from the stored list."""
        master = Master(MASTER_LIST)
        services = master.load()
        services.discard(service)
        master.save(services)


def main():
    cli = Cli()
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    name = sys.argv[2] if len(sys.argv) > 2 else None

    if cmd is None:
        cli.ls()
        return

    if cmd in ["-h", "--help"]:
        print(__doc__)
        return

    if cmd in ["-v", "--version"]:
        print(f"v{VERSION}")
        return

    if cmd in ["-r", "--rm"]:
        if name is None:
            print("Usage: master --rm NAME")
            return 1

        return cli.remove(name)

    cli.get(cmd)


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
NAME
    master — Deterministic password generator.

SYNOPSIS
    Combines `f"{username}:{password}:{service}:{counter}" to generate
    the same sha256 hash over and over again. This is then rendered
    with `-` joining each 6 characters chunks. The field `counter` is
    locked at `0` for now.

USAGE
    master                      # With no arguments, prompt for service NAME
    master SERVICE              # Gets the password for SERVICE
    master -l, --list           # Lists all stored services
    master -r, --remove NAME    # Removes service NAME from the stored list
    master -v, --version        # Shows the version
    master -h, --help           # Shows this help

ENVIRONMENT
    MASTER_USERNAME             # Username
    MASTER_PASSWORD             # Password
    MASTER_SERVICE              # Service
    MASTER_HOME                 # Config home (default: ´~/.config/master`)
    MASTER_LIST                 # Service list (default: `$MASTER_HOME/list.txt`)
    MASTER_SEPARATOR            # Chunk separator (default: `-`)
    MASTER_LENGTH               # Chunk length (default: `6`)
    MASTER_CHUNKS               # Chunk length (default: `6`)
    MASTER_DEBUG                # Prints debug decisions
"""
import os
import re
import sys
import getpass
import logging
import hashlib
import base64
import subprocess
import shutil # imports which


MASTER_VERSION   = "0.2.7"
MASTER_HOME      = os.path.expanduser("~") + "/.config/master"
MASTER_LIST      = os.environ.get("MASTER_LIST", MASTER_HOME + "/list.txt")
MASTER_USERNAME  = os.environ.get("MASTER_USERNAME", "")
MASTER_PASSWORD  = os.environ.get("MASTER_PASSWORD", "")
MASTER_SERVICE   = os.environ.get("MASTER_SERVICE", "")
MASTER_SEPARATOR = os.environ.get("MASTER_SEPARATOR", "-")
MASTER_LENGTH    = int(os.environ.get("MASTER_LENGTH", "6"))
MASTER_CHUNKS    = int(os.environ.get("MASTER_CHUNKS", "6"))
MASTER_DEBUG     = bool(os.environ.get("MASTER_DEBUG"))


class Clipboard:

    @classmethod
    def copy(cls, text: str):
        if cls.__exists("pbcopy"):
            return cls.__pbcopy(text)

        if cls.__exists("xsel"):
            return cls.__xsel(text)

        return cls.__xclip(text)


    @classmethod
    def __exists(cls, file):
        return bool(shutil.which(file))


    @classmethod
    def __pbcopy(cls, text):
        proc = subprocess.Popen(
            ["pbcopy", "w"],
            stdin=subprocess.PIPE,
            close_fds=True,
        )
        proc.communicate(input=text.encode("utf-8"))


    @classmethod
    def __xclip(cls, text):
        proc = subprocess.Popen(
            ["xclip", "-selection", "c"],
            stdin=subprocess.PIPE,
            close_fds=True
        )
        proc.communicate(input=text.encode("utf-8"))


    @classmethod
    def __xsel(cls, text):
        proc = subprocess.Popen(
            ["xsel", "-b", "-i"],
            stdin=subprocess.PIPE,
            close_fds=True
        )
        proc.communicate(input=text.encode("utf-8"))


class Master:

    def __init__(self, path: str):
        self.path = path
        self.separator = MASTER_SEPARATOR
        self.length = MASTER_LENGTH
        self.chunks = MASTER_CHUNKS

        self.services = None
        self.username = None
        self.password = None


    def load(self):
        if not self.services is None:
            return

        self.services = set()
        if not os.path.isfile(self.path):
            Logger.debug(f"File {self.path} doesn't exist")
            return

        with open(self.path, "r") as f:
            for line in f.readlines():
                self.services.add(line.strip())

        Logger.debug(f"Loaded file {self.path}")


    def add(self, service: str):
        self.load()
        return self.services.add(service)


    def remove(self, service: str):
        self.load()
        return self.services.discard(service)


    def save(self) -> bool:
        dirName = os.path.dirname(self.path)
        os.makedirs(dirName, exist_ok=True)

        with open(self.path, "w") as f:
            f.write("\n".join(self.services))
        Logger.debug(f"Wrote file {self.path}")


    def generate(self, service: str, counter: int = 0) -> str:
        source = f"{self.username}:{self.password}:{service}:{counter}"
        Logger.debug(f"Source:   {source}")
        hashed = hashlib.sha256()
        hashed.update(bytes(source, "utf8"))
        digest = hashed.digest()
        Logger.debug(f"Digest:   {digest} ({type(digest)} {len(digest)})")
        Logger.debug(f"Hex:      {digest.hex()}")
        encoded = base64.b64encode(digest).decode()
        Logger.debug(f"Encoded:  {encoded} ({type(encoded)})")

        cleaned = re.sub(r"[^0-9A-Za-z]", "", encoded)
        parts = []
        for i in range(self.chunks):
            start = i * self.length
            stop = (i + 1) * self.length
            parts.append(cleaned[start:stop])
        Logger.debug(f"Parts: {parts}")
        password = self.separator.join(parts)
        Logger.debug(f"Password: {password}")
        return password


class Logger:

    @classmethod
    def trace(cls, *largs, **dargs):
        Logger.debug(f"Trace list args: {largs}")
        Logger.debug(f"Trace dict args: {dargs}")
        def inner(func):
            Logger.debug(f"Trace hooking: {func}")
            def wrap(*args, **kwargs):
                Logger.debug(f"Trace call args: {args}")
                Logger.debug(f"Trace call kwargs: {kwargs}")
                result = func(*args, **kwargs)
                Logger.debug(f"Trace result: {result}")

                return result
            return wrap
        return inner


    @classmethod
    def debug(cls, text: str):
        if not MASTER_DEBUG: return
        print(f"\033[38;5;242m==> {text}\033[0m", file=sys.stderr)


    @classmethod
    def warn(cls, text: str):
        print(f"\033[33;1m==> {text}\033[0m", file=sys.stderr)


class Cli:

    def __init__(self):
        self.master = Master(MASTER_LIST)
        self.master.chunks = MASTER_CHUNKS
        self.master.length = MASTER_LENGTH
        self.master.separator = MASTER_SEPARATOR


    def __ask(self) -> (str, str):
        if len(MASTER_USERNAME) > 0:
            username = MASTER_USERNAME
        else:
            prompt = "Enter your master username: "
            username = getpass.getpass(prompt=prompt)

        if len(MASTER_PASSWORD) > 0:
            password = MASTER_PASSWORD
        else:
            prompt = "Enter your master password: "
            password = getpass.getpass(prompt=prompt)

        return (username, password)


    @Logger.trace("get", help="Copies the password for SERVICE.")
    def getCmd(self, *args):
        """Copies the password for SERVICE."""
        username, password = self.__ask()

        service = args[0] if len(args) > 0 else MASTER_SERVICE
        if service == "":
            service = input("Enter your service name: ")

        Logger.debug(f"Using username: {username}")
        Logger.debug(f"Using password: {password}")
        Logger.debug(f"Using service:  {service}")
        self.master.add(service)
        self.master.save()

        self.master.username = username
        self.master.password = password
        random = self.master.generate(service)
        Clipboard.copy(random)
        print(f"Password for \033[32;1m{service}\033[0m copied.")


    @Logger.trace(name="start", help="Password for a new SERVICE.")
    def startCmd(self, *args):
        """Asks input for a new SERVICE."""
        username, password = self.__ask()

        service = args[0] if len(args) > 0 else MASTER_SERVICE
        if service == "":
            service = input("Enter your service name: ")

        Logger.debug(f"Using username: {username}")
        Logger.debug(f"Using password: {password}")
        Logger.debug(f"Using service:  {service}")
        self.master.add(service)
        self.master.save()

        self.master.username = username
        self.master.password = password
        random = self.master.generate(service)
        Clipboard.copy(random)
        print(f"Password for \033[32;1m{service}\033[0m copied.")


    @Logger.trace("ls", "Lists all services.")
    def listCmd(self, *args):
        """Lists all stored services."""
        self.master.load()
        for service in self.master.services:
            print(service)


    @Logger.trace(version=MASTER_VERSION)
    def versionCmd(self, *args):
        """Prints the version."""
        Logger.debug(f"Using args: {args}")
        print(f"v{MASTER_VERSION}")


    @Logger.trace()
    def removeCmd(self, service: str, *args):
        """Removes SERVICE from the stored list."""
        self.master.remove(service)
        self.master.save()


def main():
    cli = Cli()
    name = sys.argv[1] if len(sys.argv) > 1 else "start"
    args = sys.argv[1:]

    if hasattr(cli, name + "Cmd"):
        args = sys.argv[2:]
        Logger.debug("Using the new way")
        func = getattr(cli, name + "Cmd")
        Logger.debug(f"Found name {name}: {func}({args})")
        return func(*args)

    Logger.debug("Using the old (lookup) way")
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd is None:
        return cli.startCmd()

    if cmd in ["-h", "--help", "help"]:
        return print(__doc__)

    if cmd in ["-v", "--version", "version"]:
        return cli.versionCmd()

    if cmd in ["-l","-ls", "--ls", "--list"]:
        return cli.listCmd()

    if cmd in ["-r", "--rm", "--remove", "-d", "--delete"]:
        name = args[1]
        if name is None:
            print("Usage: master --rm NAME")
            return 1

        return cli.removeCmd(args[1])

    cli.getCmd(cmd)


if __name__ == "__main__":
    exit(main())

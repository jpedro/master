import os
import sys
import click
import hashlib
import base64
import getpass
import re


class Master:

    DEBUG     = bool(os.environ.get("MASTER_DEBUG", ""))
    USERNAME  = os.environ.get("MASTER_USERNAME", "")
    PASSWORD  = os.environ.get("MASTER_PASSWORD", "")
    SEPARATOR = os.environ.get("MASTER_SEPARATOR", "-")
    LENGTH    = int(os.environ.get("MASTER_LENGTH", "6"))
    CHUNKS    = int(os.environ.get("MASTER_CHUNKS", "6"))


    def __init__(self, path: str):
        self.path = path


    def load(self) -> set:
        services = set()
        if not os.path.isfile(self.path):
            cls.debug(f"File {self.path} doesn't exit.")
            return services

        with open(path, "r") as f:
            for line in f.readlines():
                services.add(line.strip())

        self.debug(f"Loaded file {self.path}.")
        return services


    def ask(self) -> (str, str):
        if len(self.USERNAME) > 0:
            username = self.USERNAME
        else:
            prompt = "Enter your username: "
            username = getpass.getpass(prompt=prompt)

        if len(self.PASSWORD) > 0:
            password = self.PASSWORD
        else:
            prompt = "Enter your master password: "
            password = getpass.getpass(prompt=prompt)

        return (username, password)


    def save(self, services: set) -> bool:
        dirName = os.path.dirname(self.path)
        os.makedirs(dirName, exist_ok=True)

        with open(self.path, "w") as f:
            f.write("\n".join(services))
        self.debug(f"Wrote file {self.path}")


    def generate(self, service: str, chunks: int = CHUNKS, counter: int = 0) -> str:
        username, password = self.ask()
        source = f"{username}:{password}:{service}:{counter}"
        hashed = hashlib.sha256()
        hashed.update(bytes(source, "utf8"))
        encoded = base64.b64encode(hashed.digest()).decode()
        cleaned = re.sub(r"[^0-9A-Za-z]", "", encoded)
        return self.SEPARATOR.join([
            cleaned[i:i+self.LENGTH] for i in range(
                0,
                self.LENGTH * chunks,
                self.LENGTH
            )
        ])


    def debug(self, message: str) -> str:
        if not self.DEBUG:
            return

        print(f"\033[2m{message}\033[0m", file=sys.stderr)

import os
import sys
import click
import hashlib
import base64
import getpass
import re


class Master:

    DEBUG     = bool(os.environ.get("MASTER_DEBUG", ""))
    # USERNAME  = os.environ.get("USER", "Anonymous coward")
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
            self.warn(f"File {self.path} doesn't exit.")
            return services

        with open(self.path, "r") as f:
            for line in f.readlines():
                services.add(line.strip())

        self.debug(f"Loaded file {self.path}.")
        return services


    def ask(self) -> (str, str):
        if len(self.USERNAME) > 0:
            username = self.USERNAME
        else:
            prompt = "Enter your master username: "
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
        print(f"source:   {source}")
        hashed = hashlib.sha256()
        hashed.update(bytes(source, "utf8"))
        digest = hashed.digest()
        print(f"digest:   {digest} ({type(digest)} {len(digest)})")
        bb = b"d508f57bf3051ac88ced9c635bb9b290678e1207ec4df296c6b3266e0ec7e212"
        print(f"bb:       {bb} ({type(bb)} {len(bb)})")
        print(bb == digest)
        b64 = base64.b64encode(bb).decode()
        print(f"b64:      {b64}")
        encoded = base64.b64encode(digest).decode()
        print(f"encoded:  {encoded} ({type(encoded)})")

        cleaned = re.sub(r"[^0-9A-Za-z]", "", b64)
        parts = []
        for i in range(chunks):
            start = i * self.LENGTH
            stop = (i + 1) * self.LENGTH
            parts.append(cleaned[start:stop])
        print(f"parts: {parts}")
        password = self.SEPARATOR.join(parts)
        print(f"password: {password}")
        return password


    def debug(self, message: str) -> str:
        if not self.DEBUG:
            return

        print(f"\033[2m{message}\033[0m", file=sys.stderr)


    def warn(self, message: str) -> str:
        print(f"\033[33;1m{message}\033[0m", file=sys.stderr)

from dataclasses import dataclass
import json
from pathlib import Path
from typing import TypedDict, cast


@dataclass
class Credential:
    service: str
    username: str
    password: str

    def __repr__(self) -> str:
        return f"service: {self.service!r}, username: {self.username!r}, password: {self.masked_password()}"

    def masked_password(self) -> str:
        return "*" * len(self.password)

    def __str__(self) -> str:
        return f"service: {self.service}, username: {self.username}, password: {self.masked_password()}"


class CredentialData(TypedDict):
    service: str
    username: str
    password: str


class PasswordManager:
    credentials: list[Credential]
    filepath: Path

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

        if self.filepath.exists():
            self.load_credentials_from_file()
        else:
            self.credentials = []

    def load_credentials_from_file(self):
        if not self.filepath.exists():
            self.credentials = []
            return

        try:
            with self.filepath.open("r", encoding="utf-8") as file:
                raw = cast(list[CredentialData], json.load(file))
        except (OSError, json.JSONDecodeError):
            print("Coul not read due to malformed JSON.")
            self.credentials = []
            return

        self.credentials = [
            Credential(**entry)
            for entry in raw
            if {"service", "username", "password"} <= entry.keys()
        ]

    def add_credential(self, service: str, username: str, password: str):

        duplicate_found = any(
            c.service == service and c.username == username for c in self.credentials
        )
        if duplicate_found:
            raise ValueError(
                "The credential with service and username combination already exists."
            )

        self.credentials.append(Credential(service, username, password))
        self.save_credentials_to_file()

    def find_credential(self, service: str) -> Credential | None:
        for credential in self.credentials:
            if credential.service == service:
                return credential
        return None

    def delete_credential(self, service: str, username: str) -> bool:
        credentials: list[Credential] = self.credentials.copy()
        for credential in credentials:
            if credential.service == service and credential.username == username:
                self.credentials.remove(credential)
                self.save_credentials_to_file()
                return True
        return False

    def save_credentials_to_file(self):
        data = [
            {"service": c.service, "username": c.username, "password": c.password}
            for c in self.credentials
        ]

        try:
            self.filepath.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except OSError as exc:
            # Decide how to surface this (log/print/raise)
            print(f"Failed to save credentials: {exc}")


password_manager: PasswordManager = PasswordManager("credentials.json")

print(password_manager)

"""User account helpers for the JSON-backed food app."""

import hashlib
import json
import os
import secrets

USERS_FILE = "users.json"


def _read_users():
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def _write_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def _hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 bytes.fromhex(salt), 200_000).hex()
    return f"pbkdf2_sha256${salt}${digest}"


class User:
    def __init__(self, username, password, phone="", addresses=None):
        self.username = username
        self.password = password
        self.phone = phone
        self.addresses = addresses or []

    def to_record(self):
        return {"username": self.username, "password": _hash_password(self.password),
                "phone": self.phone, "addresses": self.addresses}


def register(username, password):
    users = _read_users()
    if any(user["username"].casefold() == username.casefold() for user in users):
        return False
    users.append(User(username, password).to_record())
    _write_users(users)
    return True


def authenticate(username, password):
    users = _read_users()
    for user in users:
        if user["username"].casefold() != username.casefold():
            continue
        stored = user.get("password", "")
        if stored.startswith("pbkdf2_sha256$"):
            _, salt, expected = stored.split("$", 2)
            valid = secrets.compare_digest(_hash_password(password, salt).split("$")[-1], expected)
        else:
            # Upgrade existing plaintext credentials after a successful login.
            valid = secrets.compare_digest(password, stored)
            if valid:
                user["password"] = _hash_password(password)
                _write_users(users)
        return user["username"] if valid else None
    return None


def update_profile(username, phone=None, address=None):
    users = _read_users()
    for user in users:
        if user["username"] == username:
            if phone is not None:
                user["phone"] = phone
            if address:
                addresses = user.setdefault("addresses", [])
                if address not in addresses:
                    addresses.append(address)
            _write_users(users)
            return user
    return None


def get_profile(username):
    return next((user for user in _read_users() if user["username"] == username), None)


def admin_credentials_valid(username, password):
    configured_user = os.environ.get("FOOD_APP_ADMIN_USERNAME")
    configured_password = os.environ.get("FOOD_APP_ADMIN_PASSWORD")
    return bool(configured_user and configured_password and
                secrets.compare_digest(username, configured_user) and
                secrets.compare_digest(password, configured_password))

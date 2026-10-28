import os
import secrets


class Config:
    # Generate a random development key if none is configured.
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "grimoire.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLAG_PREFIX = "OFFHA{"
    FLAG_SUFFIX = "}"
    # The admin route is disabled unless an operator configures this value.
    ADMIN_PASSCODE = os.environ.get("ADMIN_PASSCODE", "")

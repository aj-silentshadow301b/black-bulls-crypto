# Black Bulls Crypto — The Crypto Grimoire

A story-driven cryptography CTF built with Flask. Explore a 12-chapter dark-fantasy adventure, decode challenge artifacts, use progressive hints, track your score, and unlock story chapters.

> **Status:** Personal learning project. The app is intended for local, authorized training environments. It is not hardened for public hosting.

## Features

- Twelve progressive cryptography challenges, from encoding and classical ciphers to RSA and AES.
- Three levels of optional hints per challenge.
- Chapter progression, scoring, achievements, and SQLite-backed player state.
- Flask/Jinja interface with custom CSS, particle effects, and Web Audio ambience.
- JSON challenge content and a small automated test suite for flag-hash verification.

## Run locally

Requires Python 3.12 or newer.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SECRET_KEY = [guid]::NewGuid().ToString()
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). The app binds to localhost by default.

On macOS/Linux, create a virtual environment with `python3 -m venv .venv`, activate it with `source .venv/bin/activate`, then install dependencies and set `SECRET_KEY` before running `python app.py`.

## Docker

Set a private session key before starting the container:

```sh
# macOS/Linux
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

PowerShell:

```powershell
$env:SECRET_KEY = [guid]::NewGuid().ToString()
docker compose up --build
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000). Docker Compose binds the app to the container interface while keeping the published host port on localhost.

The optional admin dashboard is disabled unless `ADMIN_PASSCODE` is configured. If you enable it, use a strong, private value and keep the service on a trusted network.

## Project layout

- `app/` — Flask app factory, SQLAlchemy models, routes, and services.
- `data/` — chapter and challenge content used to seed the local database.
- `templates/` and `static/` — interface, styles, and browser-side effects.
- `tests/` — tests for normalized SHA-256 flag verification.
- `database/` — local SQLite state (created at runtime; database files are ignored).

The private author solution guide and any local database are intentionally not included in this public repository.

## Responsible use

Use the challenges only in systems and environments you own or are explicitly authorized to test. Do not expose an instance to the public internet: the project includes an admin telemetry route and is an educational prototype, not a production service. Review [SECURITY.md](SECURITY.md) before deploying or reporting a vulnerability.

## License

No license has been selected. All rights are reserved by the author unless a license is added.

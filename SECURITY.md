# Security

This repository contains an educational CTF application, not a production security product.

## Safe use

- Run locally or in an isolated lab you own or are authorized to use.
- Do not expose the app to the public internet. The admin telemetry route and player database are prototype features.
- Keep `.env`, database files, and any author-only solution materials private.
- Use a unique, randomly generated `SECRET_KEY` for persistent deployments.
- Leave `ADMIN_PASSCODE` unset unless the admin dashboard is needed; when enabled, use a strong private passcode and a trusted network.
- Do not store real personal information in this training application.

## Reporting

Please report suspected vulnerabilities privately to the repository owner before public disclosure. Include the affected route or file, impact, and clear reproduction steps. Do not include real user data or credentials in a report.

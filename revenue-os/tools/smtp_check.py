from __future__ import annotations

import os
import smtplib
import ssl
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main() -> int:
    load_env(ROOT / ".env")

    username = os.environ.get("SMTP_USERNAME", "")
    password = os.environ.get("SMTP_PASSWORD", "")
    host = os.environ.get("SMTP_HOST", "smtp.yandex.com")
    port = int(os.environ.get("SMTP_PORT", "465"))

    if not username or not password or password == "replace_with_yandex_app_password":
        print("SMTP check skipped: set SMTP_USERNAME and SMTP_PASSWORD in .env.")
        return 2

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context, timeout=20) as server:
            server.login(username, password)
            code, message = server.noop()
        if code == 250:
            print(f"SMTP login OK for {username} via {host}:{port}.")
            return 0
        print(f"SMTP login returned unexpected NOOP code: {code} {message!r}.")
        return 1
    except smtplib.SMTPAuthenticationError as exc:
        print(f"SMTP authentication failed for {username}: {exc.smtp_code}. Use a Yandex app password, not the main account password.")
        return 1
    except Exception as exc:
        print(f"SMTP check failed for {username}: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


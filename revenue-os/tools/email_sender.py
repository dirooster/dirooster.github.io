from __future__ import annotations

import argparse
import csv
import os
import smtplib
import ssl
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REVENUE_OS = ROOT / "revenue-os"
QUEUE_PATH = REVENUE_OS / "crm" / "outreach_queue.csv"
AUTH_PATH = REVENUE_OS / "config" / "authorization.yaml"
SUPPRESSION_PATH = REVENUE_OS / "crm" / "suppression.csv"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def read_bool_yaml(path: Path, key: str) -> bool:
    if not path.exists():
        return False
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip().lower() == "true"
    return False


def read_suppression() -> tuple[set[str], set[str]]:
    emails: set[str] = set()
    domains: set[str] = set()
    if not SUPPRESSION_PATH.exists():
        return emails, domains
    with SUPPRESSION_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            email = (row.get("email") or "").strip().lower()
            domain = (row.get("domain") or "").strip().lower()
            if email:
                emails.add(email)
            if domain:
                domains.add(domain)
    return emails, domains


def allowed(row: dict[str, str], suppressed_emails: set[str], suppressed_domains: set[str]) -> tuple[bool, str]:
    recipient = (row.get("recipient_email") or "").strip().lower()
    status = (row.get("status") or "").strip().lower()
    if status != "ready":
        return False, "status is not ready"
    if not recipient:
        return False, "recipient_email is empty"
    if recipient in suppressed_emails:
        return False, "recipient email is suppressed"
    domain = recipient.split("@")[-1]
    if domain in suppressed_domains:
        return False, "recipient domain is suppressed"
    return True, "ready"


def build_message(row: dict[str, str]) -> EmailMessage:
    username = os.environ["SMTP_USERNAME"]
    from_name = os.environ.get("EMAIL_FROM_NAME", "Dmitrii Petukhov")
    message = EmailMessage()
    message["From"] = f"{from_name} <{username}>"
    message["To"] = row["recipient_email"]
    message["Subject"] = row["subject"]
    if row.get("reply_to"):
        message["Reply-To"] = row["reply_to"]
    message.set_content(row["body"])
    return message


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run or send individualized outreach emails.")
    parser.add_argument("--send", action="store_true", help="Actually send ready queue items. Requires send_email: true.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of ready emails to process.")
    args = parser.parse_args()

    load_env(ROOT / ".env")
    send_authorized = read_bool_yaml(AUTH_PATH, "send_email")
    daily_limit = int(os.environ.get("DAILY_SEND_LIMIT", "10"))
    limit = min(args.limit or daily_limit, daily_limit)

    if args.send and not send_authorized:
        print("Refusing to send: config/authorization.yaml has send_email: false.")
        return 2

    if not QUEUE_PATH.exists():
        print(f"Queue not found: {QUEUE_PATH}")
        return 2

    suppressed_emails, suppressed_domains = read_suppression()
    with QUEUE_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    ready_rows: list[dict[str, str]] = []
    for row in rows:
        ok, reason = allowed(row, suppressed_emails, suppressed_domains)
        if ok:
            ready_rows.append(row)
        else:
            print(f"skip {row.get('outreach_id', '')}: {reason}")

    selected = ready_rows[:limit]
    if not selected:
        print("No ready outreach rows to process.")
        return 0

    if not args.send:
        print(f"DRY RUN: {len(selected)} messages would be processed.")
        for row in selected:
            print(f"- {row['outreach_id']} -> {row['recipient_email']} :: {row['subject']}")
        return 0

    required = ["SMTP_USERNAME", "SMTP_PASSWORD"]
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        print(f"Refusing to send: missing env vars: {', '.join(missing)}")
        return 2

    host = os.environ.get("SMTP_HOST", "smtp.yandex.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    context = ssl.create_default_context()
    sent_at = datetime.now(timezone.utc).isoformat()

    with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as server:
        server.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        for row in selected:
            server.send_message(build_message(row))
            print(f"sent {row['outreach_id']} at {sent_at}")

    print(f"Sent {len(selected)} messages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


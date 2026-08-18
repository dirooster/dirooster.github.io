# Email Setup

Mailbox:

`tech.it.rooster@yandex.ru`

## Yandex SMTP

Use a Yandex app password for Mail. Do not use the main account password.

Settings:

- SMTP host: `smtp.yandex.com`
- SMTP port: `465`
- Security: SSL
- Username: full mailbox address

Official references:

- https://yandex.com/support/id/en/authorization/app-passwords.html
- https://yandex.com/support/yandex-360/customers/mail/en/mail-clients/others.html

## Local Secret

The local `.env` file is gitignored. Fill only this value:

```env
SMTP_PASSWORD=
```

If authentication returns code `535`, create a new Yandex app password specifically for Mail and verify that SMTP access is enabled for the mailbox.

## Check Login

```powershell
python revenue-os\tools\smtp_check.py
```

Expected success:

```text
SMTP login OK for tech.it.rooster@yandex.ru via smtp.yandex.com:465.
```

## Dry Run

```powershell
python revenue-os\tools\email_sender.py --limit 5
```

## Real Sending Gate

Real sending requires all of the following:

- `config/authorization.yaml` has `send_email: true`
- queue row has `status=ready`
- queue row has `recipient_email`
- recipient is not in `crm/suppression.csv`
- command uses `--send`

```powershell
python revenue-os\tools\email_sender.py --send --limit 5
```

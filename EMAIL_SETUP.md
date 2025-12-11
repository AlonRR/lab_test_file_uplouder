# SMTP alert configuration

Set these environment variables (for example in a `.env` file) so the alert email can be sent when a file is quarantined:

- `SMTP_HOST`: SMTP server hostname.
- `SMTP_PORT`: SMTP server port (number).
- `SMTP_SENDER`: From address that will appear on the alert email.
- `ALERT_RECIPIENTS`: Comma-separated list of recipients.
- `SMTP_USERNAME`: Username for SMTP auth (optional if the server is open).
- `SMTP_PASSWORD`: Password for SMTP auth (optional).
- `SMTP_STARTTLS`: `true`/`false` to enable STARTTLS (default `true`).

Once set, any infected upload will trigger an email with the file name, S3 bucket/key, local path, and timestamp.

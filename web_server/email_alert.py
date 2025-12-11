"""Email alert helper for infected file quarantine."""

from datetime import UTC, datetime
from email.message import EmailMessage
from pathlib import Path

import aiosmtplib

from .email_config import SMTPSettings, load_smtp_settings


def _build_email_message(
    settings: SMTPSettings,
    file_path: str,
    quarantine_bucket: str,
    s3_key: str,
) -> EmailMessage:
    """Construct the alert email message body."""
    timestamp = datetime.now(tz=UTC).isoformat()
    filename = Path(file_path).name

    msg = EmailMessage()
    msg["Subject"] = f"[Alert] Infected file quarantined: {filename}"
    msg["From"] = settings.sender
    msg["To"] = ", ".join(settings.recipients)

    msg.set_content(
        (
            "An infected file was detected and quarantined.\n\n"
            f"File name: {filename}\n"
            f"Quarantine bucket: {quarantine_bucket}\n"
            f"S3 object key: {s3_key}\n"
            f"Local path: {file_path}\n"
            f"Detected at: {timestamp}\n\n"
            "Please review and take action as needed."
        ),
    )
    return msg


async def send_alert_email(
    file_path: str,
    quarantine_bucket: str,
    s3_key: str,
) -> None:
    """Send an alert email about a quarantined file."""
    settings = load_smtp_settings()
    message = _build_email_message(
        settings,
        file_path,
        quarantine_bucket,
        s3_key,
    )

    try:
        # Port 465 uses implicit TLS, port 587 uses STARTTLS
        use_tls = settings.port == 465

        smtp = aiosmtplib.SMTP(
            hostname=settings.host,
            port=settings.port,
            timeout=15,
            use_tls=use_tls,
        )
        await smtp.connect()
        print("Connected to SMTP server.")

        # Only use STARTTLS if not already using TLS and if configured
        if not use_tls and settings.use_starttls:
            await smtp.starttls()

        # Only authenticate if username is provided and non-empty
        if settings.username and settings.username.strip():
            await smtp.login(settings.username, settings.password or "")
        await smtp.send_message(message)
        await smtp.quit()
        print(
            f"Alert email sent for {s3_key} to {', '.join(settings.recipients)}.",
        )
    except Exception as exc:
        print(f"Failed to send alert email: {exc}")

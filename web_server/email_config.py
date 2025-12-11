"""SMTP configuration helpers for alert emails."""

from dataclasses import dataclass
import os
from typing import List, Optional

from dotenv import load_dotenv


@dataclass
class SMTPSettings:
    """Configuration required to send SMTP email."""

    host: str
    port: int
    sender: str
    recipients: List[str]
    username: Optional[str] = None
    password: Optional[str] = None
    use_starttls: bool = True


def _as_bool(value: str, default: bool = True) -> bool:
    """Parse common truthy/falsey strings into bool."""
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


def _parse_recipients(raw_value: str) -> List[str]:
    """Split comma-separated recipients into a clean list."""
    return [addr.strip() for addr in raw_value.split(",") if addr.strip()]


def load_smtp_settings() -> SMTPSettings:
    """Load SMTP settings from environment variables."""
    load_dotenv()

    host = os.getenv("SMTP_HOST", "")
    port = int(os.getenv("SMTP_PORT", "0"))
    sender = os.getenv("SMTP_SENDER", "")
    recipients = _parse_recipients(os.getenv("ALERT_RECIPIENTS", ""))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    use_starttls = _as_bool(os.getenv("SMTP_STARTTLS", "true"), default=True)

    if not host:
        raise ValueError("SMTP_HOST is required for sending alert emails.")
    if not port:
        raise ValueError("SMTP_PORT is required for sending alert emails.")
    if not sender:
        raise ValueError("SMTP_SENDER is required for sending alert emails.")
    if not recipients:
        raise ValueError("ALERT_RECIPIENTS must include at least one address.")

    return SMTPSettings(
        host=host,
        port=port,
        sender=sender,
        recipients=recipients,
        username=username,
        password=password,
        use_starttls=use_starttls,
    )


__all__ = ["SMTPSettings", "load_smtp_settings"]

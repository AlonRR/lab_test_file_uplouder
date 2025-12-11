# Need a scan function here, that is called by app.py after file upload
# once the file is scanned it can be uploaded to S3 using file_upload.py to either
# the quarantine or production bucket based on scan results.
# if the file is clean upload to production bucket
# if the file is infected upload to quarantine bucket and send alert email using email_alert.py
# placeholder for file scanning functionality


"""Import necessary modules for S3 interaction."""

from pathlib import Path


from aws_config import (
    production_bucket,
    quarantine_bucket,
    s3_client,
    temporary_bucket,
)

from .email_alert import send_alert_email
from .file_upload import move_file_between_buckets, upload_file_to_s3


def file_contains_string(file_path: str, search_string: str) -> bool:
    """Check if the file contains a specific string.

    Args:
        file_path: Path to the file to scan.
        search_string: String to search for in the file.
    Returns:
        bool: True if string is found, False otherwise.
    """
    with Path(file_path).open("r") as f:
        for line in f:
            if search_string in line:
                return True
    return False


def scan_file(file_path: str) -> bool:
    """Scan the uploaded file for viruses and upload to appropriate S3 bucket.

    Args:
        file_path: Path to the uploaded file.
    Returns:
        bool: True if file is clean, False if infected.
    """
    try:
        # Placeholder for actual scanning logic
        # For demonstration, let's assume files with '.pdf' are clean

        if file_path.endswith(".pdf") and file_contains_string(
            file_path,
            "Blood Sample",
        ):
            print(f"File {file_path} is clean.")
            return True
        else:
            print(f"File {file_path} is infected.")
            return False

    except Exception as e:
        print(f"Exception during file scan: {e}")


def process_file(file_path: str) -> None:
    """Process the file after receiving by scanning and moving to appropriate S3 bucket.

    Args:
        file_path: Path to the uploaded file.
    """
    upload_file_to_s3(file_path, temporary_bucket, s3_client)
    file_s3_key = Path(file_path).name
    if scan_file(file_path):
        move_file_between_buckets(
            temporary_bucket,
            production_bucket,
            file_s3_key,
            s3_client,
        )
    else:
        move_file_between_buckets(
            temporary_bucket,
            quarantine_bucket,
            file_s3_key,
            s3_client,
        )
        send_alert_email(file_path, quarantine_bucket, file_s3_key)
    Path(file_path).unlink()

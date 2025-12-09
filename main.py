from datetime import datetime

from AWS_config import production_bucket, quarantine_bucket, s3_client
from web_server.app import start_server


def pre_start_checks() -> None:
    """Perform pre-start checks for S3 connectivity."""
    try:
        s3_client.head_bucket(Bucket=quarantine_bucket)
        print(f"S3 bucket '{quarantine_bucket}' is accessible.")
    except Exception as e:
        print(
            f"Error accessing S3 bucket '{quarantine_bucket}': {e}",
        )
        raise
    try:
        s3_client.head_bucket(Bucket=production_bucket)
        print(f"S3 bucket '{production_bucket}' is accessible.")
    except Exception as e:
        print(
            f"Error accessing S3 bucket '{production_bucket}': {e}",
        )
        raise
    try:
        now = datetime.now(datetime.timezone.utc)
        print(
            f"S3 connectivity check successful at {now.isoformat()} UTC.",
        )
    except Exception as e:
        print(f"Error fetching time from S3: {e}")
        raise
    print("Pre-start checks completed successfully.")


def start_process() -> None:
    """Start main process after pre-start checks."""
    print("Starting main process...")
    start_server()


if __name__ == "__main__":
    pre_start_checks()
    start_process()

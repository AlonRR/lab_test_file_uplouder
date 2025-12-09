from datetime import datetime

from AWS_config import s3_client
from web_server.app import start_server


def pre_start_loads() -> tuple:
    """Load S3 configuration and create client."""
    client, bucket = s3_client()
    return client, bucket


def pre_start_checks() -> None:
    """Perform pre-start checks for S3 connectivity."""
    try:
        client.head_bucket(Bucket=bucket)
        print(f"S3 bucket '{bucket}' is accessible.")
    except Exception as e:
        print(f"Error accessing S3 bucket '{bucket}': {e}")
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
    client, bucket = pre_start_loads()
    pre_start_checks()
    start_process()

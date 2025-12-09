from datetime import datetime

from AWS_config import S3Config
from web_server.app import start_server


def pre_start_loads() -> S3Config:
    """Load S3 configuration and create client."""
    return S3Config.load_s3_config()


def pre_start_checks() -> None:
    """Perform pre-start checks for S3 connectivity."""
    try:
        client.head_bucket()
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
    client = pre_start_loads()
    pre_start_checks()
    start_process()
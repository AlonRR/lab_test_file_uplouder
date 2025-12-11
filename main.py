from datetime import UTC, datetime

# from aws_config import (
#     production_bucket,
#     quarantine_bucket,
#     s3_client,
#     temporary_bucket,
# )
from web_server.app import start_server

# def pre_start_checks() -> None:
#     """Perform pre-start checks for S3 connectivity."""

#     try:
#         now = datetime.now(tz=UTC)
#         print(
#             f"S3 connectivity check successful at {now.isoformat()} UTC.",
#         )
#     except Exception as e:
#         print(f"Error fetching time from S3: {e}")
#         raise
#     print("Pre-start checks completed successfully.")


def start_process() -> None:
    """Start main process after pre-start checks."""
    print("Starting main process...")
    start_server()


if __name__ == "__main__":
    # pre_start_checks()
    start_process()

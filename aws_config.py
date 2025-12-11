import os

import boto3
from dotenv import load_dotenv


class S3Config:
    """Class to hold S3 configuration."""

    def __init__(self) -> None:
        """Initialize S3Config with necessary parameters."""
        load_dotenv()
        access_key = os.getenv("S3_ACCESS_KEY")
        secret_key = os.getenv("S3_SECRET_KEY")
        region = os.getenv("S3_REGION")
        self.__quarantine_bucket = os.getenv("QUARANTINE_BUCKET")
        self.__production_bucket = os.getenv("PRODUCTION_BUCKET")
        self.__temporary_bucket = os.getenv("TEMPORARY_BUCKET")
        self.__client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    @property
    def quarantine_bucket(self) -> str:
        """Get the quarantine bucket name."""
        return self.__quarantine_bucket

    @property
    def production_bucket(self) -> str:
        """Get the production bucket name."""
        return self.__production_bucket

    @property
    def temporary_bucket(self) -> str:
        """Get the temporary bucket name."""
        return self.__temporary_bucket

    @property
    def client(self) -> boto3.client:
        """Get the S3 client."""
        return self.__client

    def __self_test__(self) -> None:
        """Self test to verify S3 connectivity."""
        try:
            self.client.list_buckets()
            print("S3 client initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize S3 client: {e}")
            raise

s3_config = S3Config()
s3_config.__self_test__()
s3_client = s3_config.client
quarantine_bucket = s3_config.quarantine_bucket
production_bucket = s3_config.production_bucket
temporary_bucket = s3_config.temporary_bucket

__all__ = [
    "production_bucket",
    "quarantine_bucket",
    "s3_client",
    "temporary_bucket",
]

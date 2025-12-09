import os

import boto3
from dotenv import load_dotenv


def load_s3_config() -> tuple:
    """Load S3 configuration from .env file."""
    load_dotenv()
    bucket = os.getenv("S3_BUCKET")
    access_key = os.getenv("S3_ACCESS_KEY")
    secret_key = os.getenv("S3_SECRET_KEY")
    region = os.getenv("S3_REGION")

    return bucket, access_key, secret_key, region


def s3_client() -> tuple:
    """Create and return an S3 client using environment variables."""
    bucket, access_key, secret_key, region = load_s3_config()
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )
    return (
        s3_client,
        bucket,
    )

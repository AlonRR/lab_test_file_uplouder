from datetime import UTC, datetime
from pathlib import Path


def upload_file_to_s3(
    file_path: str,
    s3_bucket: str,
    s3_client: any,
) -> None:
    """Upload file_path to S3.

    Args:
        file_path: Local path to the file to upload.
        s3_bucket: Target S3 bucket name.
        s3_client: Boto3 S3 client instance.
    """
    basename = Path(file_path).name
    try:
        s3_client.upload_file(file_path, s3_bucket, basename)
        print(
            f"File {file_path} uploaded to bucket {s3_bucket} as {basename}.",
        )
    except Exception as e:
        print(f"Upload failed: {e}")
        raise


def move_file_between_buckets(
    source_bucket: str,
    destination_bucket: str,
    file_s3_key: str,
    s3_client: any,
) -> None:
    """Move a file from source_bucket to destination_bucket in S3.

    Args:
        source_bucket: The S3 bucket to move the file from.
        destination_bucket: The S3 bucket to move the file to.
        file_s3_key: The key of the file in S3.
        s3_client: Boto3 S3 client instance.
    """
    try:
        s3_client.copy_object(
            CopySource={
                "Bucket": source_bucket,
                "Key": file_s3_key,
            },
            Bucket=destination_bucket,
            Key=file_s3_key,
        )
        s3_client.delete_object(Bucket=source_bucket, Key=file_s3_key)
        print(
            f"File {file_s3_key} moved from {source_bucket} to {destination_bucket}.",
        )
    except Exception as e:
        print(f"Failed to move file {file_s3_key}: {e}")
        raise

from datetime import datetime
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
    name, ext = Path(basename).stem, Path(basename).suffix
    time_stamp = datetime.timezone.utc.strftime("%Y%m%d%H%M%S")
    s3_key = f"{name}_{time_stamp}{ext}"

    try:
        s3_client.put_object(Bucket=s3_bucket, Key=file_path)
        print(
            f"File {file_path} uploaded to bucket {s3_bucket} as {s3_key}.",
        )
    except Exception as e:
        print(f"Upload failed: {e}")
        raise

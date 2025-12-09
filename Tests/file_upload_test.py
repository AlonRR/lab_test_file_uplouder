# Test file upload
import os
from pathlib import Path

from dotenv import load_dotenv

from AWS_config import s3_client
from web_server.file_upload import upload_file_to_s3

load_dotenv()
production_bucket = os.getenv("PRODUCTION_BUCKET")
quarantine_bucket = os.getenv("QUARANTINE_BUCKET")
client = s3_client()

# Create a test file
test_file_path = "../web_server/pending_files/testfile.pdf"
Path(test_file_path).touch()
with Path(test_file_path).open("w") as f:
    f.write("This is a test file for S3 upload.")

# Upload to production bucket
try:
    upload_file_to_s3(
        test_file_path,
        production_bucket,
        client,
    )
    Path(test_file_path).unlink()
    print(
        f"Test file upload and clean up successful to {production_bucket}.",
    )
except Exception as e:
    print(f"An error occurred: {e}")
    raise

# Upload to quarantine bucket
try:
    upload_file_to_s3(
        test_file_path,
        quarantine_bucket,
        client,
    )
    Path(test_file_path).unlink()
    print(
        f"Test file upload and clean up successful to {quarantine_bucket}.",
    )

except Exception as e:
    print(f"An error occurred: {e}")
    raise

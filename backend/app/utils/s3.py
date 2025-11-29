"""S3 utility functions with test-settings fallback."""

import boto3
from botocore.exceptions import ClientError

# Try real settings, fallback to test settings (just like logger.py)
try:
    from backend.app.core.config import settings
except Exception:
    from backend.app.core.test_settings import settings

from backend.app.utils.logger import logger

# Initialize S3 client (DigitalOcean Spaces compatible)
s3_client = boto3.client(
    "s3",
    region_name=settings.DO_SPACES_REGION,
    endpoint_url=f"https://{settings.DO_SPACES_REGION}.digitaloceanspaces.com",
    aws_access_key_id=settings.DO_SPACES_KEY,
    aws_secret_access_key=settings.DO_SPACES_SECRET,
)


def upload_file(file_data: bytes, key: str) -> bool:
    """Upload a file to S3."""
    try:
        s3_client.put_object(
            Bucket=settings.DO_SPACES_BUCKET,
            Key=key,
            Body=file_data,
        )
        logger.info(f"Uploaded to S3: {key}")
        return True
    except ClientError as err:  # noqa: BLE001
        logger.error(f"S3 upload failed: {err}")
        return False


def download_file(key: str) -> bytes:
    """Download a file from S3."""
    try:
        response = s3_client.get_object(
            Bucket=settings.DO_SPACES_BUCKET,
            Key=key,
        )
        return response["Body"].read()
    except ClientError as err:  # noqa: BLE001
        logger.error(f"S3 download failed: {err}")
        raise


def delete_file(key: str) -> bool:
    """Delete a file from S3."""
    try:
        s3_client.delete_object(
            Bucket=settings.DO_SPACES_BUCKET,
            Key=key,
        )
        return True
    except ClientError as err:  # noqa: BLE001
        logger.error(f"S3 delete failed: {err}")
        return False

import boto3
from botocore.exceptions import ClientError

from config.aws_config import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    REGION,
    BUCKET_NAME
)


def get_s3_client():
    """
    Create and return an S3 client.
    """

    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION
    )


def upload_file(local_file, s3_key):
    """
    Upload a local parquet file to S3.

    Parameters
    ----------
    local_file : str
        Local parquet file path.

    s3_key : str
        Destination object key in S3.
    """

    s3 = get_s3_client()

    try:
        s3.upload_file(
            local_file,
            BUCKET_NAME,
            s3_key
        )

        print("=" * 60)
        print("Upload Successful")
        print(f"Bucket : {BUCKET_NAME}")
        print(f"S3 Key : {s3_key}")
        print("=" * 60)

    except ClientError as e:
        print("=" * 60)
        print("S3 Upload Failed")
        print(e)
        print("=" * 60)
        raise
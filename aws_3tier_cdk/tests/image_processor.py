# aws_3tier_cdk/tests/image_processor.py
import boto3
from botocore.exceptions import ClientError

# Option 1: Module-level S3 client
boto3_client = boto3.client("s3")

def download_image(bucket: str, key: str) -> bytes:
    """
    Downloads an image from S3 and returns it as bytes.
    """
    if not bucket or not key:
        raise ValueError("Bucket and key must be provided")
    
    try:
        response = boto3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    except ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            raise FileNotFoundError(f"{key} does not exist in {bucket}")
        elif e.response['Error']['Code'] == "AccessDenied":
            raise PermissionError("Access denied to S3 bucket")
        else:
            raise e

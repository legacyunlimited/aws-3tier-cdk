
import json
import boto3
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')

THUMBNAIL_SIZE = (128, 128)

def handler(event, context):
    bucket_name = event['bucket']
    key = event['key']

    response = s3.get_object(Bucket=bucket_name, Key=key)
    image_content = response['Body'].read()
    
    # Load image
    image = Image.open(BytesIO(image_content))
    
    # Extract metadata
    metadata = image.info
    
    # Resize original
    resized_image = image.resize((800, 800))
    buffer = BytesIO()
    resized_image.save(buffer, format=image.format)
    buffer.seek(0)
    
    resized_key = f"resized/{key}"
    s3.put_object(Bucket=bucket_name, Key=resized_key, Body=buffer)

    # Create thumbnail
    image.thumbnail(THUMBNAIL_SIZE)
    thumb_buffer = BytesIO()
    image.save(thumb_buffer, format=image.format)
    thumb_buffer.seek(0)
    
    thumb_key = f"thumbnails/{key}"
    s3.put_object(Bucket=bucket_name, Key=thumb_key, Body=thumb_buffer)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'original_key': key,
            'resized_key': resized_key,
            'thumbnail_key': thumb_key,
            'metadata': metadata
        })
    }

import boto3
import re
import io
from PIL import Image
from datetime import datetime
import uuid
import base64
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Hardcoded values instead of ENV
OUTPUT_BUCKET = 'serverless-image-s3-storage'
DYNAMO_TABLE = 'Images'

def lambda_handler(event, context):
    try:
        # Clean and decode base64 image
        raw_b64 = re.sub(r'\s+', '', event['body'])
        if len(raw_b64) % 4 != 0:
            raw_b64 += '=' * (4 - len(raw_b64) % 4)
        image_data = base64.b64decode(raw_b64)

        # Open and process image
        image = Image.open(io.BytesIO(image_data))
        processed_image = image.convert("L").resize((512, 512))

        # Generate ID and save to S3
        image_id = str(uuid.uuid4())
        processed_key = f"processed/{image_id}.png"
        buffer = io.BytesIO()
        processed_image.save(buffer, format="PNG")
        buffer.seek(0)

        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=processed_key,
            Body=buffer,
            ContentType='image/png'
        )

        # Store metadata in DynamoDB
        table = dynamodb.Table(DYNAMO_TABLE)
        table.put_item(Item={
            'ID': image_id,
            'Filename': processed_key,
            'Timestamp': datetime.utcnow().isoformat(),
            'Status': 'processed',
            'Size': buffer.getbuffer().nbytes,
            'Format': 'PNG'
        })

        logger.info(f"✅ Image processed and stored: {processed_key}")
        return {
            'statusCode': 200,
            'body': f"Image processed and stored as {processed_key}"
        }

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error processing image: {str(e)}"
        }

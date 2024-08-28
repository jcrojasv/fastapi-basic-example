import boto3
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET')
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
AWS_REGION = os.getenv('AWS_REGION')


logger.info(f"Connecting to S3 bucket: {AWS_S3_BUCKET}")
logger.info(f"AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID}")
logger.info(f"AWS_SECRET_ACCESS_KEY: {AWS_SECRET_ACCESS_KEY}")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)
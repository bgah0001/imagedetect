import numpy as np
from object_detection import ObjectDetector
import io
from PIL import Image

import json
import boto3
import logging
import time
import numpy as np



logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        # Log the event for debugging purposes
        logger.info("Event: %s", json.dumps(event))

        # Extract bucket name and object key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        # Get the image from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        im_bytes = response['Body'].read()
        im_file = io.BytesIO(im_bytes)  
        img = Image.open(im_file)
        img = np.array(img)
        objectDetector = ObjectDetector()

        
        objects = objectDetector.detectImage(img)

        
        tags = ', '.join({obj['label'] for obj in objects})


        # Generate unique Image_id using current timestamp
        image_id = str(int(time.time()))
        
        # Construct the S3 image URL
        uri = f's3://{bucket_name}/{object_key}'

        # Insert data into DynamoDB table
        table = dynamodb.Table('Images_Tags_Objects')
     
        table.put_item(
            Item={
                'Image_id': image_id,
                'uri': uri,
                'tags': tags
            }
        )
        data = {
            'Items': 'Tags updated successfully',
            'Image_id': image_id,
            'uri': uri,
            'tags': tags
        }

        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    except Exception as e:
        logger.error("Error processing S3 event: %s", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


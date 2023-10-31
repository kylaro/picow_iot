import json
import boto3
from decimal import Decimal
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Parse the incoming JSON payload
    print("event:",event)
    
    body = json.loads(event['body'])
    
    # Extract data and convert to Decimal
    co2 = str(body.get('co2'))
    humidity = str(body.get('humidity'))
    temperature = str(body.get('temperature'))

    # Your IoT device's unique identifier
    device_id = 'Test3'  # Replace with actual device ID logic

    # Current timestamp as sort key
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # DynamoDB table name
    table_name = 'IoTData'

    # Write data to DynamoDB
    table = dynamodb.Table(table_name)
    item = {
           'device_id': device_id,
           'timestamp': timestamp,
           'co2': co2,
           'humidity': humidity,
           'temperature': temperature
       }
    print("Putting in DYNAMODB:", item)
    response = table.put_item(
       Item=item
    )
    
    

    return {
        'statusCode': 201,
        'body': json.dumps('Data successfully written to DynamoDB')
    }

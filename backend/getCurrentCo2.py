import boto3
import json
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from dateutil.parser import parse

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table_name = "MakeSureToBackup"
    device_id = "Test3"  # Ideally, this should be dynamic or validated

    try:
        table = dynamodb.Table(table_name)

        # Query for the most recent sample
        response = table.query(
            KeyConditionExpression=Key('device_id').eq(device_id),
            ScanIndexForward=False,  # This orders the results in descending order
            Limit=1
        )

        latest_item = response.get('Items', [])[0] if response.get('Items') else None
        if not latest_item:
            return {
                'statusCode': 200,
                'body': json.dumps("No data available")
            }

        # Parse the timestamp from the latest item
        latest_timestamp = parse(latest_item['timestamp'])
        
        # Calculate the start timestamp for the last 2 minutes
        start_timestamp = (latest_timestamp - timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')

        # Query DynamoDB for readings from the last 2 minutes
        response = table.query(
            KeyConditionExpression=Key('device_id').eq(device_id) & 
                                    Key('timestamp').gte(start_timestamp)
        )
        
        items = response.get('Items', [])
        print("ITEMS = ", items)
        print("LEN = ", len(items))

        # Check if there are readings
        if not items:
            return {
                'statusCode': 200,
                'body': json.dumps("device off")
            }

        # Calculate the average CO2
        total_co2 = sum(float(item['co2']) for item in items)  # Ensure your items have a 'co2' key
        average_co2 = int(total_co2 / len(items))
        print("AVERAGE = ", average_co2)

        return {
            'statusCode': 200,
            'body': json.dumps({"averageCO2": average_co2})
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Internal server error"})
        }

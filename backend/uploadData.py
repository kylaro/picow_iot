import json
import boto3
from decimal import Decimal
from datetime import datetime
from zoneinfo import ZoneInfo

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')


def increment_counter():
    table_name = "GlobalCounter"
    
    table = dynamodb.Table(table_name)
    
    response = table.update_item(
        Key={
            'counter_id': 'sample_count'
        },
        UpdateExpression='SET #cnt = #cnt + :val',
        ExpressionAttributeNames={
            '#cnt': 'count'  # 'count' is the actual attribute name
        },
        ExpressionAttributeValues={
            ':val': 1
        },
        ReturnValues="UPDATED_NEW"
    )
    
def get_counter():
    table_name = "GlobalCounter"
    
    table = dynamodb.Table(table_name)
    
    response = table.get_item(Key={'counter_id':'sample_count'})
    
    item = response.get('Item')

    return item['count']
    


def lambda_handler(event, context):
    # Parse the incoming JSON payload
    #print("event:",event)
    #global counter
    #print("COUNT: ", counter)
    #counter += 1
    body = json.loads(event['body'])
    
    # Extract data and convert to Decimal
    co2 = str(body.get('co2'))
    humidity = str(body.get('humidity'))
    temperature = str(body.get('temperature'))

    # Your IoT device's unique identifier
    device_id = 'Test3'  # Replace with actual device ID logic

    # Current timestamp as sort key
    timestamp = datetime.now()  # This gets the current datetime without formatting it into a string

    # Get the current time in the Paris/Netherlands time zone
    paris_time = datetime.now(ZoneInfo("Europe/Amsterdam"))
    
    # Format the time into a string if needed
    timestamp = paris_time.strftime('%Y-%m-%d %H:%M:%S')

    
    print(timestamp)
    #check_paris_time()

    # DynamoDB table name
    table_name = 'MakeSureToBackup'

    # Write data to DynamoDB
    table = dynamodb.Table(table_name)
    item = {
           'device_id': device_id,
           'timestamp': timestamp,
           'co2': co2,
           'humidity': humidity,
           'temperature': temperature
       }
       
    
    #print("Putting in DYNAMODB:", item)
    # Ignore if this is the test item:
    #co2 564.0, \"humidity\": 69.972, \"temperature\": 18.341
    if co2 == "564.0" and humidity == "69.972" and temperature == "18.341":
        print("caught test item")
    else:
        #handle_resample()
        response = table.put_item(
           Item=item
        )
    
    

    return {
        'statusCode': 201,
        'body': json.dumps('Data successfully written to DynamoDB')
    }

import boto3
import json
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')

cache = {
    ""
}

def resample_data(original_list, target_length):
    if not original_list or target_length <= 0:
        return []

    if target_length >= len(original_list):
        return original_list.copy()

    # Calculate the step size
    step = len(original_list) / target_length

    # Resample the list by selecting the closest element
    resampled_list = []
    for i in range(target_length):
        index = int(round(i * step))
        # Ensure the index is within the bounds of the original list
        index = min(index, len(original_list) - 1)
        resampled_list.append(original_list[index])

    return resampled_list


# def resample_data(items, target_points=500):
#     n = len(items)
#     if n <= target_points:
#         # If the number of items is exactly 500, just return them
#         return items
#     elif n > target_points:
#         # Downsample: Select every nth item
#         step = n / target_points
#         return [items[int(i * step)] for i in range(target_points)]

def lambda_handler(event, context):
    print("event:", event)
    table_name = "IoTData"
    device_id = "Test3"  # Ideally, this should be dynamic or validated

    time_range = event.get('queryStringParameters', {}).get('range', '1 day')
    start_timestamp = calculate_start_timestamp(time_range)

    try:
        table = dynamodb.Table(table_name)

        if time_range != 'All':
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('device_id').eq(device_id) & 
                                        boto3.dynamodb.conditions.Key('timestamp').gte(start_timestamp)
            )
        else:
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('device_id').eq(device_id)
            )

        items = response['Items']
        
        items = resample_data(items, 400)
        

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Internal server error"})
        }

def calculate_start_timestamp(time_range):
    now = datetime.now()
    time_dict = {
        '15 minutes': timedelta(minutes=15),
        '1 hour': timedelta(hours=1),
        '6 hours': timedelta(hours=6),
        '12 hours': timedelta(hours=12),
        '1 day': timedelta(days=1),
        '7 days': timedelta(days=7),
        '30 days': timedelta(days=30),
        '3 months': timedelta(days=90),  # Approximation: 3 months as 90 days
        '1 year': timedelta(days=365),    # Not accounting for leap year
        #'All': timedelta.max
    }
    if time_range not in time_dict.keys():
        time_range = "1 day"
    start = now - time_dict.get(time_range, timedelta(hours=1))
    return start.strftime('%Y-%m-%d %H:%M:%S')

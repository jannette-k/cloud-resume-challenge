import os
import boto3
import json

# import requests

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    response = table.update_item(
        Key={'id' : 'visitor_count'},
        UpdateExpression="ADD #count :inc",
        ExpressionAttributeNames={
            '#count': 'count'
        }, # "count" needs an alias, it's a reserved word in DynamoDB
        ExpressionAttributeValues={':inc': 1},
        ReturnValues="UPDATED_NEW"
    )

    new_count = response['Attributes']['count']

    return {
        "statusCode": 200,
        "headers" :
        {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"  # the CORS header — allows your domain to call this
        },
        'body': json.dumps({'count': int(new_count)})
    }

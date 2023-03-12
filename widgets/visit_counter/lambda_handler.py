import os
import time

import boto3

TableName = os.environ['TableName']
client = boto3.client('dynamodb')

def lambda_handler(event, context):
    print('RECIVE', dict(event))
    method = event['requestContext']['http']['method']
    origin = event['headers']['origin']
    x_page = event['headers']['x-referer-page']

    key = {'page': {'S': origin + x_page}}
    EMPTY_RESP = {'last_visit': {'N': 0},'visit': {'N': 0}}

    if method == 'GET':
        resp = client.get_item(
            TableName=TableName,
            Key=key
        )
        d = resp.get('Item', EMPTY_RESP)
        data = {
            'last': d['last_visit']['N'],
            'visit': d['visit']['N'],
        }
    elif method == 'POST':
        now = int(time.time())
        resp = client.update_item(
            TableName=TableName,
            Key=key,
            UpdateExpression='SET last_visit = :time ADD visit :inc',
            ExpressionAttributeValues={':inc': {'N': '1'}, ':time': {'N': str(now)}},
            ReturnValues="UPDATED_OLD"
        )
        d = resp.get('Attributes', EMPTY_RESP)
        data = {
            'last': d['last_visit']['N'],
            'visit': str(int(d['visit']['N']) + 1),
        }
    else:
        data = {}

    print('SEND', data)
    return data

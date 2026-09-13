# tests/test_app.py
import boto3
import pytest
from moto import mock_aws  # simulates AWS services in memory — no real AWS calls, no cost
from hello_world.app import lambda_handler

TABLE_NAME = 'janet-resume-visitor-count'


@pytest.fixture
def dynamodb_table():
    """Creates a fake DynamoDB table in memory before each test, and tears it down after."""
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        yield table  # test runs here


def test_counter_increments_from_zero(dynamodb_table):
    """First-ever visit: counter should go from nothing to 1."""
    response = lambda_handler({}, {})

    assert response['statusCode'] == 200
    body = response['body']
    assert '"count": 1' in body


def test_counter_increments_on_repeated_calls(dynamodb_table):
    """Simulates 3 separate visits — count should end up at 3, not reset each time."""
    lambda_handler({}, {})
    lambda_handler({}, {})
    third_response = lambda_handler({}, {})

    assert '"count": 3' in third_response['body']


def test_response_has_cors_header(dynamodb_table):
    """Makes sure the CORS header is present — without it, your frontend JS would be blocked."""
    response = lambda_handler({}, {})

    assert 'Access-Control-Allow-Origin' in response['headers']


def test_response_is_valid_json(dynamodb_table):
    """Confirms the body is actually parseable JSON, not just a string that looks like it."""
    import json
    response = lambda_handler({}, {})

    parsed = json.loads(response['body'])
    assert isinstance(parsed['count'], int)
"""Sample AWS Lambda handler that triggers conditional steering.

This file demonstrates a Python Lambda function that imports boto3 and
handles AWS events. When working on this file in Kiro, the conditional
steering file `aws-patterns.md` (globs: **/*.py) will automatically
activate, providing AWS best practices guidance.

This is a sample file for demonstration purposes only.
All values use placeholders — no real credentials or account IDs.
"""

import json
import logging
from typing import Any

import boto3
from botocore.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use explicit session for testability (as recommended by aws-patterns steering)
TABLE_NAME = "your-table-name"
REGION = "us-east-1"

retry_config = Config(retries={"max_attempts": 3, "mode": "adaptive"})


def get_dynamodb_client():
    """Create a DynamoDB client with retry configuration."""
    session = boto3.Session(region_name=REGION)
    return session.client("dynamodb", config=retry_config)


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Lambda handler that processes API Gateway events.

    Reads an item from DynamoDB and returns it as a JSON response.

    Args:
        event: API Gateway proxy event.
        context: Lambda context object.

    Returns:
        API Gateway proxy response with status code and body.
    """
    logger.info("Received event: %s", json.dumps(event))

    # Extract item ID from path parameters
    path_params = event.get("pathParameters") or {}
    item_id = path_params.get("id")

    if not item_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'id' path parameter"}),
        }

    client = get_dynamodb_client()

    try:
        response = client.get_item(
            TableName=TABLE_NAME,
            Key={"id": {"S": item_id}},
        )
    except client.exceptions.ResourceNotFoundException:
        logger.warning("Table %s not found", TABLE_NAME)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
        }

    item = response.get("Item")
    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": f"Item '{item_id}' not found"}),
        }

    # Convert DynamoDB item to plain dict
    result = {k: list(v.values())[0] for k, v in item.items()}

    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }

"""AWS utility functions for DynamoDB and Bedrock client initialization.

Task 1.2: Create AWS helper utilities (DynamoDB client, Bedrock client)
"""

import os

import boto3


def get_dynamodb_table():
    """Get DynamoDB table resource using environment configuration.

    Returns:
        boto3 DynamoDB Table resource for the conversations table.
    """
    table_name = os.environ.get("TABLE_NAME", "ConversationsTable")
    region = os.environ.get("AWS_REGION", "us-east-1")

    dynamodb = boto3.resource("dynamodb", region_name=region)
    return dynamodb.Table(table_name)


def get_bedrock_client():
    """Get Bedrock Runtime client for model invocation.

    Returns:
        boto3 Bedrock Runtime client.
    """
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("bedrock-runtime", region_name=region)


def get_model_id() -> str:
    """Get the Bedrock model ID from environment configuration.

    Returns:
        Model ID string for Bedrock invocation.
    """
    return os.environ.get("MODEL_ID", "us.anthropic.claude-sonnet-4-20250514")

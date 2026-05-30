"""Integration tests for API endpoints with mocked AWS services.

Task 5.2: Write integration tests for API endpoints
Uses moto to mock DynamoDB and patches Bedrock calls.
"""

import json
import os
from unittest.mock import MagicMock, patch

import boto3
import pytest
from moto import mock_aws


@pytest.fixture(autouse=True)
def aws_env(monkeypatch):
    """Set up environment variables for tests."""
    monkeypatch.setenv("TABLE_NAME", "ConversationsTable")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("MODEL_ID", "us.anthropic.claude-sonnet-4-20250514")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture
def dynamodb_table():
    """Create a mocked DynamoDB table."""
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="ConversationsTable",
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="ConversationsTable")
        yield table


@pytest.fixture
def mock_bedrock_response():
    """Mock Bedrock client response."""
    mock_client = MagicMock()
    response_body = json.dumps({"content": [{"text": "I can help with that!"}]})
    mock_response = MagicMock()
    mock_response.read.return_value = response_body.encode()
    mock_client.invoke_model.return_value = {"body": mock_response}
    return mock_client


class TestChatEndpoint:
    """Integration tests for POST /chat."""

    @mock_aws
    @patch("src.core.assistant.get_bedrock_client")
    def test_successful_chat_new_session(self, mock_bedrock_fn, mock_bedrock_response):
        """Test a successful chat request that creates a new session."""
        # Set up DynamoDB
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName="ConversationsTable",
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        mock_bedrock_fn.return_value = mock_bedrock_response

        from src.handlers.chat_handler import lambda_handler

        event = {
            "body": json.dumps({"message": "What is serverless?"}),
            "requestContext": {"http": {"method": "POST"}},
        }
        context = MagicMock()
        context.aws_request_id = "test-request-id"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["response"] == "I can help with that!"
        assert "session_id" in body
        assert "timestamp" in body

    @mock_aws
    @patch("src.core.assistant.get_bedrock_client")
    def test_chat_with_existing_session(self, mock_bedrock_fn, mock_bedrock_response):
        """Test a chat request with an existing session ID."""
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName="ConversationsTable",
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        mock_bedrock_fn.return_value = mock_bedrock_response

        from src.handlers.chat_handler import lambda_handler

        event = {
            "body": json.dumps({"message": "Follow up", "session_id": "my-session-123"}),
            "requestContext": {"http": {"method": "POST"}},
        }
        context = MagicMock()
        context.aws_request_id = "test-request-id"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["session_id"] == "my-session-123"

    def test_chat_missing_message(self):
        """Test that missing message returns 400."""
        from src.handlers.chat_handler import lambda_handler

        event = {
            "body": json.dumps({}),
            "requestContext": {"http": {"method": "POST"}},
        }
        context = MagicMock()
        context.aws_request_id = "test-request-id"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "message is required" in body["error"]

    def test_chat_invalid_json(self):
        """Test that invalid JSON returns 400."""
        from src.handlers.chat_handler import lambda_handler

        event = {
            "body": "not valid json{{{",
            "requestContext": {"http": {"method": "POST"}},
        }
        context = MagicMock()
        context.aws_request_id = "test-request-id"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "Invalid JSON" in body["error"]

    def test_chat_empty_message(self):
        """Test that empty message returns 400."""
        from src.handlers.chat_handler import lambda_handler

        event = {
            "body": json.dumps({"message": "   "}),
            "requestContext": {"http": {"method": "POST"}},
        }
        context = MagicMock()
        context.aws_request_id = "test-request-id"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 400


class TestHistoryEndpoint:
    """Integration tests for GET /history/{session_id}."""

    @mock_aws
    def test_get_history_with_messages(self):
        """Test retrieving history for a session with messages."""
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="ConversationsTable",
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Insert test messages
        table.put_item(Item={
            "session_id": "test-session",
            "timestamp": "2024-01-01T00:00:00+00:00",
            "role": "user",
            "content": "Hello",
        })
        table.put_item(Item={
            "session_id": "test-session",
            "timestamp": "2024-01-01T00:00:01+00:00",
            "role": "assistant",
            "content": "Hi there!",
        })

        from src.handlers.history_handler import lambda_handler

        event = {
            "pathParameters": {"session_id": "test-session"},
            "requestContext": {"http": {"method": "GET"}},
        }
        context = MagicMock()
        context.aws_request_id = "test-request-id"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["session_id"] == "test-session"
        assert len(body["messages"]) == 2
        assert body["messages"][0]["role"] == "user"
        assert body["messages"][1]["role"] == "assistant"

    @mock_aws
    def test_get_history_empty_session(self):
        """Test retrieving history for a session with no messages."""
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        dynamodb.create_table(
            TableName="ConversationsTable",
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        from src.handlers.history_handler import lambda_handler

        event = {
            "pathParameters": {"session_id": "nonexistent-session"},
            "requestContext": {"http": {"method": "GET"}},
        }
        context = MagicMock()
        context.aws_request_id = "test-request-id"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["session_id"] == "nonexistent-session"
        assert body["messages"] == []

    def test_get_history_missing_session_id(self):
        """Test that missing session_id returns 400."""
        from src.handlers.history_handler import lambda_handler

        event = {
            "pathParameters": {},
            "requestContext": {"http": {"method": "GET"}},
        }
        context = MagicMock()
        context.aws_request_id = "test-request-id"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "Invalid session_id" in body["error"]

"""Unit tests for core assistant business logic.

Task 5.1: Write unit tests for core business logic
Tests message processing, model formatting, and data model behavior.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.core.assistant import (
    create_response,
    generate_session_id,
    get_conversation_history,
    invoke_bedrock,
    store_message,
)
from src.core.models import ChatMessage, ChatResponse, ConversationHistory


# --- Data Model Tests ---


class TestChatMessage:
    """Tests for the ChatMessage dataclass."""

    def test_create_user_message(self):
        msg = ChatMessage(role="user", content="Hello", timestamp="2024-01-01T00:00:00+00:00")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.timestamp == "2024-01-01T00:00:00+00:00"

    def test_create_assistant_message(self):
        msg = ChatMessage(role="assistant", content="Hi there!")
        assert msg.role == "assistant"
        assert msg.content == "Hi there!"
        assert msg.timestamp  # Auto-generated

    def test_to_dict(self):
        msg = ChatMessage(role="user", content="Test", timestamp="2024-01-01T00:00:00+00:00")
        result = msg.to_dict()
        assert result == {
            "role": "user",
            "content": "Test",
            "timestamp": "2024-01-01T00:00:00+00:00",
        }

    def test_from_dict(self):
        data = {"role": "assistant", "content": "Response", "timestamp": "2024-01-01T12:00:00+00:00"}
        msg = ChatMessage.from_dict(data)
        assert msg.role == "assistant"
        assert msg.content == "Response"
        assert msg.timestamp == "2024-01-01T12:00:00+00:00"


class TestChatResponse:
    """Tests for the ChatResponse dataclass."""

    def test_to_dict(self):
        resp = ChatResponse(
            response="AI answer",
            session_id="abc-123",
            timestamp="2024-01-01T00:00:00+00:00",
        )
        result = resp.to_dict()
        assert result == {
            "response": "AI answer",
            "session_id": "abc-123",
            "timestamp": "2024-01-01T00:00:00+00:00",
        }


class TestConversationHistory:
    """Tests for the ConversationHistory dataclass."""

    def test_empty_history(self):
        history = ConversationHistory(session_id="test-session")
        result = history.to_dict()
        assert result == {"session_id": "test-session", "messages": []}

    def test_history_with_messages(self):
        messages = [
            ChatMessage(role="user", content="Hi", timestamp="2024-01-01T00:00:00+00:00"),
            ChatMessage(role="assistant", content="Hello!", timestamp="2024-01-01T00:00:01+00:00"),
        ]
        history = ConversationHistory(session_id="sess-1", messages=messages)
        result = history.to_dict()
        assert len(result["messages"]) == 2
        assert result["messages"][0]["role"] == "user"
        assert result["messages"][1]["role"] == "assistant"


# --- Business Logic Tests ---


class TestGenerateSessionId:
    """Tests for session ID generation."""

    def test_generates_uuid_format(self):
        session_id = generate_session_id()
        # UUID4 format: 8-4-4-4-12 hex characters
        parts = session_id.split("-")
        assert len(parts) == 5
        assert len(parts[0]) == 8

    def test_generates_unique_ids(self):
        ids = {generate_session_id() for _ in range(100)}
        assert len(ids) == 100


class TestCreateResponse:
    """Tests for the create_response function."""

    @patch("src.core.assistant.store_message")
    @patch("src.core.assistant.invoke_bedrock")
    def test_creates_response_with_new_session(self, mock_bedrock, mock_store):
        mock_bedrock.return_value = "AI response text"

        result = create_response(message="Hello")

        assert result.response == "AI response text"
        assert result.session_id  # Generated
        assert result.timestamp
        assert mock_store.call_count == 2  # User + assistant messages

    @patch("src.core.assistant.store_message")
    @patch("src.core.assistant.invoke_bedrock")
    def test_creates_response_with_existing_session(self, mock_bedrock, mock_store):
        mock_bedrock.return_value = "Response"

        result = create_response(message="Hi", session_id="existing-session")

        assert result.session_id == "existing-session"

    def test_raises_on_empty_message(self):
        with pytest.raises(ValueError, match="message is required"):
            create_response(message="")

    def test_raises_on_whitespace_message(self):
        with pytest.raises(ValueError, match="message is required"):
            create_response(message="   ")

    def test_raises_on_none_message(self):
        with pytest.raises(ValueError, match="message is required"):
            create_response(message=None)


class TestInvokeBedrock:
    """Tests for Bedrock invocation."""

    @patch("src.core.assistant.get_model_id")
    @patch("src.core.assistant.get_bedrock_client")
    def test_successful_invocation(self, mock_client_fn, mock_model_id):
        mock_model_id.return_value = "us.anthropic.claude-sonnet-4-20250514"
        mock_client = MagicMock()
        mock_client_fn.return_value = mock_client

        # Mock the response body
        response_body = json.dumps({"content": [{"text": "Hello from Bedrock!"}]})
        mock_response = MagicMock()
        mock_response.read.return_value = response_body.encode()
        mock_client.invoke_model.return_value = {"body": mock_response}

        result = invoke_bedrock("Test message")

        assert result == "Hello from Bedrock!"
        mock_client.invoke_model.assert_called_once()

    @patch("src.core.assistant.get_model_id")
    @patch("src.core.assistant.get_bedrock_client")
    def test_raises_on_failure(self, mock_client_fn, mock_model_id):
        mock_model_id.return_value = "us.anthropic.claude-sonnet-4-20250514"
        mock_client = MagicMock()
        mock_client_fn.return_value = mock_client
        mock_client.invoke_model.side_effect = Exception("Service unavailable")

        with pytest.raises(RuntimeError, match="Bedrock invocation failed"):
            invoke_bedrock("Test")


class TestStoreMessage:
    """Tests for message persistence."""

    @patch("src.core.assistant.get_dynamodb_table")
    def test_stores_message_successfully(self, mock_table_fn):
        mock_table = MagicMock()
        mock_table_fn.return_value = mock_table

        msg = ChatMessage(role="user", content="Hello", timestamp="2024-01-01T00:00:00+00:00")
        store_message("session-123", msg)

        mock_table.put_item.assert_called_once_with(
            Item={
                "session_id": "session-123",
                "timestamp": "2024-01-01T00:00:00+00:00",
                "role": "user",
                "content": "Hello",
            }
        )

    @patch("src.core.assistant.get_dynamodb_table")
    def test_raises_on_dynamodb_failure(self, mock_table_fn):
        mock_table = MagicMock()
        mock_table_fn.return_value = mock_table
        mock_table.put_item.side_effect = Exception("DynamoDB error")

        msg = ChatMessage(role="user", content="Hello", timestamp="2024-01-01T00:00:00+00:00")

        with pytest.raises(RuntimeError, match="Failed to save message"):
            store_message("session-123", msg)


class TestGetConversationHistory:
    """Tests for history retrieval."""

    @patch("src.core.assistant.get_dynamodb_table")
    def test_returns_messages_in_order(self, mock_table_fn):
        mock_table = MagicMock()
        mock_table_fn.return_value = mock_table
        mock_table.query.return_value = {
            "Items": [
                {"role": "user", "content": "Hi", "timestamp": "2024-01-01T00:00:00+00:00"},
                {"role": "assistant", "content": "Hello!", "timestamp": "2024-01-01T00:00:01+00:00"},
            ]
        }

        history = get_conversation_history("session-123")

        assert history.session_id == "session-123"
        assert len(history.messages) == 2
        assert history.messages[0].role == "user"
        assert history.messages[1].role == "assistant"

    @patch("src.core.assistant.get_dynamodb_table")
    def test_returns_empty_for_unknown_session(self, mock_table_fn):
        mock_table = MagicMock()
        mock_table_fn.return_value = mock_table
        mock_table.query.return_value = {"Items": []}

        history = get_conversation_history("nonexistent")

        assert history.session_id == "nonexistent"
        assert history.messages == []

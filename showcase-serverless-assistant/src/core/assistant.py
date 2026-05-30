"""Core business logic for the AI assistant.

Task 2.1: Implement create_response() function with Bedrock integration
Task 2.2: Implement conversation persistence logic
"""

import json
import uuid
from datetime import datetime, timezone

from src.core.models import ChatMessage, ChatResponse, ConversationHistory
from src.utils.aws_helpers import get_bedrock_client, get_dynamodb_table, get_model_id


def generate_session_id() -> str:
    """Generate a new unique session ID."""
    return str(uuid.uuid4())


def create_response(message: str, session_id: str | None = None) -> ChatResponse:
    """Process a user message and generate an AI response.

    Orchestrates the full chat flow: validates input, calls Bedrock,
    persists messages, and returns the response.

    Args:
        message: The user's input message.
        session_id: Optional existing session ID. Generated if not provided.

    Returns:
        ChatResponse with the AI response, session_id, and timestamp.

    Raises:
        ValueError: If message is empty or None.
        RuntimeError: If Bedrock invocation fails.
    """
    if not message or not message.strip():
        raise ValueError("message is required")

    if session_id is None:
        session_id = generate_session_id()

    # Generate timestamp for this interaction
    timestamp = datetime.now(timezone.utc).isoformat()

    # Create user message
    user_message = ChatMessage(role="user", content=message.strip(), timestamp=timestamp)

    # Call Bedrock for AI response
    ai_response_text = invoke_bedrock(message.strip())

    # Create assistant message with slightly later timestamp
    assistant_timestamp = datetime.now(timezone.utc).isoformat()
    assistant_message = ChatMessage(
        role="assistant", content=ai_response_text, timestamp=assistant_timestamp
    )

    # Persist both messages to DynamoDB
    store_message(session_id, user_message)
    store_message(session_id, assistant_message)

    return ChatResponse(
        response=ai_response_text,
        session_id=session_id,
        timestamp=assistant_timestamp,
    )


def invoke_bedrock(message: str) -> str:
    """Invoke Amazon Bedrock to generate an AI response.

    Args:
        message: The user message to send to the model.

    Returns:
        The generated response text.

    Raises:
        RuntimeError: If the Bedrock API call fails.
    """
    client = get_bedrock_client()
    model_id = get_model_id()

    request_body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": message}],
        }
    )

    try:
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=request_body,
        )

        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]

    except Exception as e:
        raise RuntimeError(f"Bedrock invocation failed: {e}") from e


def store_message(session_id: str, message: ChatMessage) -> None:
    """Persist a message to DynamoDB.

    Args:
        session_id: The conversation session ID (partition key).
        message: The ChatMessage to store.

    Raises:
        RuntimeError: If the DynamoDB write fails.
    """
    table = get_dynamodb_table()

    try:
        table.put_item(
            Item={
                "session_id": session_id,
                "timestamp": message.timestamp,
                "role": message.role,
                "content": message.content,
            }
        )
    except Exception as e:
        raise RuntimeError(f"Failed to save message: {e}") from e


def get_conversation_history(session_id: str) -> ConversationHistory:
    """Retrieve all messages for a session from DynamoDB.

    Args:
        session_id: The conversation session ID to query.

    Returns:
        ConversationHistory with messages ordered by timestamp ascending.
    """
    table = get_dynamodb_table()

    response = table.query(
        KeyConditionExpression="session_id = :sid",
        ExpressionAttributeValues={":sid": session_id},
        ScanIndexForward=True,  # Sort by timestamp ascending
    )

    messages = [ChatMessage.from_dict(item) for item in response.get("Items", [])]
    return ConversationHistory(session_id=session_id, messages=messages)

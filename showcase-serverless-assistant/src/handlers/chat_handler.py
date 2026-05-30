"""Lambda handler for the chat endpoint (POST /chat).

Task 3.1: Implement chat_handler Lambda (POST /chat)

Receives a user message, generates an AI response via Bedrock,
stores both messages in DynamoDB, and returns the response.
"""

import json
import logging

from src.core.assistant import create_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST,OPTIONS",
    "Content-Type": "application/json",
}


def lambda_handler(event, context):
    """Handle POST /chat requests.

    Expected request body:
        {
            "message": "User's question",
            "session_id": "optional-session-id"
        }

    Returns:
        {
            "response": "AI-generated answer",
            "session_id": "session-uuid",
            "timestamp": "2024-01-01T00:00:00+00:00"
        }
    """
    logger.info("Chat request received", extra={"request_id": context.aws_request_id})

    # Handle CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

    # Parse request body
    try:
        body = json.loads(event.get("body", "{}"))
    except (json.JSONDecodeError, TypeError):
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Invalid JSON in request body"}),
        }

    # Validate required fields
    message = body.get("message")
    if not message or not str(message).strip():
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "message is required"}),
        }

    session_id = body.get("session_id")

    # Process the message
    try:
        chat_response = create_response(message=str(message), session_id=session_id)

        logger.info(
            "Chat response generated",
            extra={"session_id": chat_response.session_id},
        )

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(chat_response.to_dict()),
        }

    except ValueError as e:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)}),
        }

    except RuntimeError as e:
        error_msg = str(e)
        if "Bedrock" in error_msg:
            logger.error("Bedrock invocation failed", extra={"error": error_msg})
            return {
                "statusCode": 502,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "AI service unavailable"}),
            }
        else:
            logger.error("Internal error", extra={"error": error_msg})
            return {
                "statusCode": 500,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Failed to save message"}),
            }

    except Exception as e:
        logger.error("Unexpected error", extra={"error": str(e)})
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Internal server error"}),
        }

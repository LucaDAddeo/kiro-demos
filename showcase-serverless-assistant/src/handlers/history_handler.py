"""Lambda handler for the conversation history endpoint (GET /history/{session_id}).

Task 3.2: Implement history_handler Lambda (GET /history/{session_id})

Retrieves all messages for a given session from DynamoDB,
ordered by timestamp ascending.
"""

import json
import logging

from src.core.assistant import get_conversation_history

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Content-Type": "application/json",
}


def lambda_handler(event, context):
    """Handle GET /history/{session_id} requests.

    Path parameters:
        session_id: The conversation session ID to retrieve.

    Returns:
        {
            "session_id": "session-uuid",
            "messages": [
                {"role": "user", "content": "...", "timestamp": "..."},
                {"role": "assistant", "content": "...", "timestamp": "..."}
            ]
        }
    """
    logger.info(
        "History request received", extra={"request_id": context.aws_request_id}
    )

    # Handle CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

    # Extract session_id from path parameters
    path_params = event.get("pathParameters") or {}
    session_id = path_params.get("session_id")

    if not session_id or not session_id.strip():
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Invalid session_id"}),
        }

    try:
        history = get_conversation_history(session_id=session_id.strip())

        logger.info(
            "History retrieved",
            extra={
                "session_id": session_id,
                "message_count": len(history.messages),
            },
        )

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(history.to_dict()),
        }

    except Exception as e:
        logger.error("Failed to retrieve history", extra={"error": str(e)})
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Failed to retrieve conversation history"}),
        }

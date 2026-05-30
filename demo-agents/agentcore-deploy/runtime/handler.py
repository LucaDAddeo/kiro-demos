"""AgentCore Runtime Handler.

Processes incoming requests for the AgentCore-deployed cloud operations agent.
This handler is invoked by the AgentCore runtime and manages the agent's
request/response lifecycle.

Deployment:
    Deployed via AgentCore using agent_config.yaml configuration.
"""

import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_request(event: dict) -> dict:
    """Process an incoming agent request.

    This is the main entry point for the AgentCore runtime. It receives
    user messages, processes them through the agent logic, and returns
    structured responses.

    Args:
        event: AgentCore request event containing:
            - session_id: Unique session identifier
            - input_text: User's message
            - session_attributes: Optional session context

    Returns:
        dict: Response with agent output and session metadata.
    """
    logger.info("Processing request: %s", json.dumps(event))

    session_id = event.get("session_id", "unknown")
    input_text = event.get("input_text", "")
    session_attributes = event.get("session_attributes", {})

    # Validate input
    if not input_text.strip():
        return _build_response(
            session_id=session_id,
            output_text="Please provide a question or command about your AWS resources.",
            status="REQUIRES_INPUT"
        )

    # Route to appropriate handler based on intent
    intent = _classify_intent(input_text)

    if intent == "cost_analysis":
        output = _handle_cost_analysis(input_text, session_attributes)
    elif intent == "resource_listing":
        output = _handle_resource_listing(input_text, session_attributes)
    elif intent == "help":
        output = _handle_help()
    else:
        output = _handle_general(input_text)

    return _build_response(
        session_id=session_id,
        output_text=output,
        status="COMPLETED"
    )


def _classify_intent(input_text: str) -> str:
    """Classify the user's intent from their input text.

    Args:
        input_text: The user's message.

    Returns:
        str: Classified intent category.
    """
    text_lower = input_text.lower()

    if any(word in text_lower for word in ["cost", "spend", "bill", "expense", "budget"]):
        return "cost_analysis"
    elif any(word in text_lower for word in ["list", "resource", "inventory", "show"]):
        return "resource_listing"
    elif any(word in text_lower for word in ["help", "what can you", "capabilities"]):
        return "help"
    else:
        return "general"


def _handle_cost_analysis(input_text: str, session_attributes: dict) -> str:
    """Handle cost analysis requests.

    In production, this delegates to the AnalyzeCosts action group.
    """
    region = session_attributes.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    return (
        f"I'll analyze your AWS costs in {region}. "
        "Invoking the cost analysis tool to get your spending breakdown "
        "and optimization recommendations."
    )


def _handle_resource_listing(input_text: str, session_attributes: dict) -> str:
    """Handle resource listing requests.

    In production, this delegates to the ListResources action group.
    """
    region = session_attributes.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    return (
        f"I'll list your active AWS resources in {region}. "
        "Invoking the resource listing tool to get your current inventory."
    )


def _handle_help() -> str:
    """Return help information about agent capabilities."""
    return (
        "I'm your cloud operations assistant. I can help you with:\n\n"
        "1. **Cost Analysis** — Analyze your AWS spending by service, "
        "identify trends, and suggest optimizations.\n"
        "2. **Resource Listing** — List active resources in your account, "
        "filtered by region or service.\n\n"
        "Try asking: 'What are my top spending services this month?' or "
        "'List all Lambda functions in us-east-1'."
    )


def _handle_general(input_text: str) -> str:
    """Handle general queries that don't match specific intents."""
    return (
        "I can help with AWS cost analysis and resource management. "
        "Could you be more specific? For example:\n"
        "- 'Analyze my costs for the last 30 days'\n"
        "- 'List resources in us-east-1'\n"
        "- 'What are my most expensive services?'"
    )


def _build_response(session_id: str, output_text: str, status: str) -> dict:
    """Build a structured response for the AgentCore runtime.

    Args:
        session_id: Session identifier.
        output_text: Agent's response text.
        status: Response status (COMPLETED, REQUIRES_INPUT, ERROR).

    Returns:
        dict: Formatted response for AgentCore.
    """
    return {
        "session_id": session_id,
        "output_text": output_text,
        "status": status,
        "metadata": {
            "agent_name": "cloud-ops-agent",
            "model_id": os.environ.get("MODEL_ID", "us.anthropic.claude-sonnet-4-20250514")
        }
    }

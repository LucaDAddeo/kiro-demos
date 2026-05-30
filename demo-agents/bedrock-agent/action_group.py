"""Bedrock Agent Action Group — Lambda Handler.

This Lambda function processes action group requests from a Bedrock Agent.
It handles two actions:
  - AnalyzeCosts: Returns cost analysis data for the specified AWS account.
  - ListResources: Lists active AWS resources in the specified region.

Deployment:
    Deploy via SAM template at infra/template.yaml
"""

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context) -> dict:
    """Process Bedrock Agent action group invocations.

    Args:
        event: Bedrock Agent action group event containing:
            - actionGroup: Name of the action group
            - apiPath: The API path being invoked
            - httpMethod: HTTP method (GET, POST)
            - parameters: List of parameter objects
            - requestBody: Request body content (for POST)
        context: Lambda context object.

    Returns:
        dict: Action group response with statusCode and body.
    """
    logger.info("Received event: %s", json.dumps(event))

    action_group = event.get("actionGroup", "")
    api_path = event.get("apiPath", "")
    http_method = event.get("httpMethod", "GET")
    parameters = event.get("parameters", [])

    # Extract parameters into a dict for easier access
    params = {p["name"]: p["value"] for p in parameters}

    if api_path == "/analyze-costs":
        response_body = _handle_analyze_costs(params)
    elif api_path == "/list-resources":
        response_body = _handle_list_resources(params)
    else:
        response_body = {
            "error": f"Unknown API path: {api_path}",
            "supportedPaths": ["/analyze-costs", "/list-resources"]
        }

    # Format response for Bedrock Agent
    action_response = {
        "actionGroup": action_group,
        "apiPath": api_path,
        "httpMethod": http_method,
        "httpStatusCode": 200,
        "responseBody": {
            "application/json": {
                "body": json.dumps(response_body)
            }
        }
    }

    api_response = {
        "messageVersion": "1.0",
        "response": action_response
    }

    logger.info("Returning response: %s", json.dumps(api_response))
    return api_response


def _handle_analyze_costs(params: dict) -> dict:
    """Handle the AnalyzeCosts action.

    Args:
        params: Dictionary with optional keys:
            - region: AWS region (default: us-east-1)
            - days: Number of days to analyze (default: 30)

    Returns:
        dict: Cost analysis summary.
    """
    region = params.get("region", "us-east-1")
    days = int(params.get("days", "30"))

    # In production, this would call AWS Cost Explorer API
    # For demo purposes, return structured sample data
    return {
        "region": region,
        "period_days": days,
        "total_cost_usd": 142.57,
        "top_services": [
            {"service": "Amazon Bedrock", "cost_usd": 45.20, "percentage": 31.7},
            {"service": "AWS Lambda", "cost_usd": 28.90, "percentage": 20.3},
            {"service": "Amazon DynamoDB", "cost_usd": 22.15, "percentage": 15.5},
            {"service": "Amazon S3", "cost_usd": 18.40, "percentage": 12.9},
            {"service": "Amazon CloudWatch", "cost_usd": 12.80, "percentage": 9.0}
        ],
        "recommendations": [
            "Consider Reserved Capacity for Bedrock if usage is consistent",
            "Review Lambda memory allocation — some functions may be over-provisioned",
            "Enable S3 Intelligent-Tiering for infrequently accessed objects"
        ]
    }


def _handle_list_resources(params: dict) -> dict:
    """Handle the ListResources action.

    Args:
        params: Dictionary with optional keys:
            - region: AWS region (default: us-east-1)
            - service: Filter by service name (optional)

    Returns:
        dict: List of active resources.
    """
    region = params.get("region", "us-east-1")
    service_filter = params.get("service", None)

    # In production, this would call AWS Resource Groups Tagging API
    # For demo purposes, return structured sample data
    resources = [
        {"service": "Lambda", "name": "chat-handler", "arn": "arn:aws:lambda:us-east-1:123456789012:function:chat-handler"},
        {"service": "Lambda", "name": "history-handler", "arn": "arn:aws:lambda:us-east-1:123456789012:function:history-handler"},
        {"service": "DynamoDB", "name": "conversations", "arn": "arn:aws:dynamodb:us-east-1:123456789012:table/conversations"},
        {"service": "S3", "name": "agent-artifacts", "arn": "arn:aws:s3:::agent-artifacts-123456789012"},
        {"service": "Bedrock", "name": "cloud-ops-agent", "arn": "arn:aws:bedrock:us-east-1:123456789012:agent/AGENTID123"}
    ]

    if service_filter:
        resources = [r for r in resources if r["service"].lower() == service_filter.lower()]

    return {
        "region": region,
        "resource_count": len(resources),
        "resources": resources
    }

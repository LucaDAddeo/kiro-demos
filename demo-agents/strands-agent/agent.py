"""Strands Agents SDK example — Cloud Operations Agent.

Demonstrates a Strands Agent using BedrockModel with a custom tool
that integrates with cloud-ops-toolkit for cost analysis.

Usage:
    python agent.py

Requires:
    - AWS credentials configured (AWS_PROFILE or environment variables)
    - cloud-ops-toolkit available at the path specified in .env
"""

import json
import os
import subprocess

from strands import Agent, tool
from strands.models import BedrockModel


@tool
def analyze_costs(profile: str = "your-profile-name", region: str = "us-east-1") -> dict:
    """Analyze AWS costs using cloud-ops-toolkit.

    Delegates to cloud-ops-toolkit/scripts/finops/cost-analysis.sh
    via subprocess. See cloud-ops-toolkit docs/integrations.md for details.

    Args:
        profile: AWS CLI profile name to use for cost analysis.
        region: AWS region to analyze costs for.

    Returns:
        dict: Cost analysis results as JSON, or error details.
    """
    toolkit_path = os.environ.get("TOOLKIT_PATH", "../cloud-ops-toolkit")
    script_path = os.path.join(toolkit_path, "scripts", "finops", "cost-analysis.sh")

    if not os.path.exists(script_path):
        return {
            "error": f"cloud-ops-toolkit not found at {toolkit_path}",
            "hint": "Clone cloud-ops-toolkit or set TOOLKIT_PATH in .env"
        }

    try:
        result = subprocess.run(
            [script_path, "--profile", profile, "--region", region, "--json"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr.strip(), "returncode": result.returncode}

    except subprocess.TimeoutExpired:
        return {"error": "Cost analysis timed out after 60 seconds"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON output from cost-analysis.sh", "raw": result.stdout}
    except FileNotFoundError:
        return {"error": f"Script not found: {script_path}"}


def create_agent() -> Agent:
    """Create and configure the Strands Agent with BedrockModel."""
    model = BedrockModel(model_id=os.environ.get("MODEL_ID", "us.anthropic.claude-sonnet-4-20250514"))
    agent = Agent(model=model, tools=[analyze_costs])
    return agent


if __name__ == "__main__":
    agent = create_agent()

    # Sample prompt demonstrating the agent's cost analysis capability
    prompt = (
        "Analyze the AWS costs for my account in us-east-1. "
        "Summarize the top spending services and suggest optimizations."
    )

    print(f"Prompt: {prompt}")
    print("-" * 60)

    response = agent(prompt)
    print(response)

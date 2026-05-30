"""Custom tools for the Strands Cloud Operations Agent.

These tools integrate with cloud-ops-toolkit scripts via subprocess,
following the patterns documented in cloud-ops-toolkit/docs/integrations.md.

The toolkit is referenced as a Git submodule — scripts are never copied
into this repository.
"""

import json
import os
import subprocess

from strands import tool


@tool
def analyze_costs(profile: str = "your-profile-name", region: str = "us-east-1") -> dict:
    """Analyze AWS costs using cloud-ops-toolkit.

    Delegates to cloud-ops-toolkit/scripts/finops/cost-analysis.sh
    via subprocess. See cloud-ops-toolkit docs/integrations.md for details.

    The script returns JSON output with cost breakdown by service,
    trends, and optimization recommendations.

    Args:
        profile: AWS CLI profile name to use for cost analysis.
        region: AWS region to analyze costs for.

    Returns:
        dict: Cost analysis results as JSON, or error details.
    """
    toolkit_path = os.environ.get("CLOUD_OPS_TOOLKIT_PATH", "../cloud-ops-toolkit")
    script_path = os.path.join(toolkit_path, "scripts", "finops", "cost-analysis.sh")

    if not os.path.exists(script_path):
        return {
            "status": "error",
            "error": f"cloud-ops-toolkit not found at {toolkit_path}",
            "hint": (
                "Clone cloud-ops-toolkit as a submodule: "
                "git submodule add https://github.com/your-org/cloud-ops-toolkit.git"
            )
        }

    try:
        result = subprocess.run(
            [script_path, "--profile", profile, "--region", region, "--json"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        elif result.returncode == 1:
            return {"status": "error", "type": "input_error", "message": result.stderr.strip()}
        elif result.returncode == 2:
            return {"status": "error", "type": "aws_error", "message": result.stderr.strip()}
        elif result.returncode == 3:
            return {"status": "error", "type": "dependency_missing", "message": result.stderr.strip()}
        else:
            return {"status": "error", "returncode": result.returncode, "message": result.stderr.strip()}

    except subprocess.TimeoutExpired:
        return {"status": "error", "type": "timeout", "message": "Cost analysis timed out after 60 seconds"}
    except json.JSONDecodeError:
        return {"status": "error", "type": "parse_error", "message": "Invalid JSON output from cost-analysis.sh"}
    except FileNotFoundError:
        return {"status": "error", "type": "not_found", "message": f"Script not found: {script_path}"}

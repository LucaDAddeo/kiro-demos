#!/usr/bin/env bash
# Local development script for the Serverless Assistant.
# Uses SAM CLI to run the API locally with hot-reload support.
#
# Prerequisites:
#   - AWS SAM CLI installed (https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
#   - Docker running (for Lambda container emulation)
#   - Python 3.11+
#
# Usage:
#   ./local-dev.sh              # Start local API on port 3000
#   ./local-dev.sh --port 8080  # Start on custom port

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="${SCRIPT_DIR}/infra"
PORT="${1:-3000}"

# Check prerequisites
if ! command -v sam &> /dev/null; then
    echo "ERROR: AWS SAM CLI not found. Install from:"
    echo "  https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html"
    exit 1
fi

if ! docker info &> /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Start Docker Desktop and try again."
    exit 1
fi

echo "=== Serverless Assistant — Local Development ==="
echo ""
echo "Building SAM application..."
sam build --template-file "${INFRA_DIR}/template.yaml" --use-container

echo ""
echo "Starting local API on http://localhost:${PORT}"
echo "Press Ctrl+C to stop."
echo ""
echo "Endpoints:"
echo "  POST http://localhost:${PORT}/chat"
echo "  GET  http://localhost:${PORT}/history/{session_id}"
echo ""

sam local start-api \
    --template-file "${INFRA_DIR}/template.yaml" \
    --port "${PORT}" \
    --warm-containers EAGER \
    --env-vars <(cat <<EOF
{
    "ChatFunction": {
        "TABLE_NAME": "assistant-conversations-dev",
        "MODEL_ID": "us.anthropic.claude-sonnet-4-20250514",
        "AWS_REGION": "us-east-1"
    },
    "HistoryFunction": {
        "TABLE_NAME": "assistant-conversations-dev",
        "AWS_REGION": "us-east-1"
    }
}
EOF
)

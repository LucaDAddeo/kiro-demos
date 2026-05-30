#!/usr/bin/env bash
# Teardown script for the Serverless Assistant.
# Removes all AWS resources created by the SAM deployment.
#
# Usage:
#   ./teardown.sh              # Delete dev stack
#   ./teardown.sh staging      # Delete staging stack
#   ./teardown.sh prod         # Delete prod stack (requires confirmation)
#
# WARNING: This permanently deletes all resources including DynamoDB data.

set -euo pipefail

ENVIRONMENT="${1:-dev}"
STACK_NAME="serverless-assistant-${ENVIRONMENT}"
REGION="${AWS_REGION:-us-east-1}"
PROFILE="${AWS_PROFILE:-your-profile-name}"

echo "=== Serverless Assistant — Teardown ==="
echo ""
echo "Stack:       ${STACK_NAME}"
echo "Region:      ${REGION}"
echo "Profile:     ${PROFILE}"
echo "Environment: ${ENVIRONMENT}"
echo ""

# Extra confirmation for production
if [[ "${ENVIRONMENT}" == "prod" ]]; then
    echo "⚠️  WARNING: You are about to delete the PRODUCTION stack!"
    echo "    This will permanently delete all conversation data."
    echo ""
    read -rp "Type 'DELETE PRODUCTION' to confirm: " confirmation
    if [[ "${confirmation}" != "DELETE PRODUCTION" ]]; then
        echo "Aborted."
        exit 1
    fi
fi

echo "Deleting CloudFormation stack: ${STACK_NAME}..."
echo ""

sam delete \
    --stack-name "${STACK_NAME}" \
    --region "${REGION}" \
    --profile "${PROFILE}" \
    --no-prompts

echo ""
echo "✅ Stack '${STACK_NAME}' deleted successfully."
echo "   All Lambda functions, API Gateway, DynamoDB table, and IAM roles removed."

#!/usr/bin/env bash
# teardown.sh — Delete all deployed agent demo resources
# Usage: ./teardown.sh [--profile your-profile-name] [--region us-east-1]

set -euo pipefail

PROFILE="${AWS_PROFILE:-your-profile-name}"
REGION="${AWS_REGION:-us-east-1}"
STACK_NAME="demo-agents-stack"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --profile) PROFILE="$2"; shift 2 ;;
        --region) REGION="$2"; shift 2 ;;
        --stack-name) STACK_NAME="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: ./teardown.sh [--profile PROFILE] [--region REGION] [--stack-name STACK]"
            echo ""
            echo "Deletes the SAM stack and all associated AWS resources."
            echo ""
            echo "Options:"
            echo "  --profile     AWS CLI profile (default: \$AWS_PROFILE or 'your-profile-name')"
            echo "  --region      AWS region (default: \$AWS_REGION or 'us-east-1')"
            echo "  --stack-name  CloudFormation stack name (default: 'demo-agents-stack')"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo "=== Agent Demos Teardown ==="
echo "Profile: ${PROFILE}"
echo "Region:  ${REGION}"
echo "Stack:   ${STACK_NAME}"
echo ""

# Confirm before deletion
read -rp "Are you sure you want to delete all resources? (y/N): " confirm
if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "Deleting SAM stack '${STACK_NAME}'..."
sam delete \
    --stack-name "${STACK_NAME}" \
    --region "${REGION}" \
    --profile "${PROFILE}" \
    --no-prompts

echo ""
echo "Stack deletion initiated. Monitor progress:"
echo "  aws cloudformation describe-stacks --stack-name ${STACK_NAME} --profile ${PROFILE} --region ${REGION}"
echo ""
echo "Teardown complete. All resources will be removed within a few minutes."

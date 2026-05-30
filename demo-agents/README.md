# Agent Workflows Demo

**Execution mode:** Deployable

This demo showcases three AI agent development patterns on AWS, each integrating with [cloud-ops-toolkit](https://github.com/your-org/cloud-ops-toolkit) for operational automation.

## Agent Patterns

### 1. Strands Agents SDK (`strands-agent/`)

A Python agent built with the [Strands Agents SDK](https://github.com/strands-agents/sdk-python) using Amazon Bedrock as the model provider.

**Architecture:**
```
User Prompt → Strands Agent → BedrockModel (Claude)
                   ↓
            analyze_costs tool
                   ↓
     cloud-ops-toolkit/scripts/finops/cost-analysis.sh
```

- `agent.py` — Agent initialization with BedrockModel
- `tools.py` — Custom `analyze_costs` tool that invokes cloud-ops-toolkit via subprocess
- `requirements.txt` — Pinned dependencies

### 2. Bedrock Agents (`bedrock-agent/`)

A managed agent using Amazon Bedrock Agents with a Lambda-backed action group.

**Architecture:**
```
User → Bedrock Agent → Action Group (Lambda)
                            ↓
                   AnalyzeCosts / ListResources
                            ↓
                   Cost Explorer / Resource Groups API
```

- `action_group.py` — Lambda handler processing agent action group requests
- `agent-schema.json` — OpenAPI schema defining the action group API
- `requirements.txt` — Pinned dependencies

### 3. AgentCore Deployment (`agentcore-deploy/`)

Deployment configuration for Amazon Bedrock AgentCore, providing managed infrastructure for running agents.

**Architecture:**
```
AgentCore Runtime → Agent Handler → Tool Invocations
       ↓                                    ↓
  Session Memory              cloud-ops-toolkit scripts
```

- `agent_config.yaml` — AgentCore deployment configuration (model, tools, memory, guardrails)
- `runtime/handler.py` — Agent runtime handler processing requests

## Cloud-Ops-Toolkit Integration

The agent tools invoke cloud-ops-toolkit scripts via subprocess rather than duplicating them. Set up the toolkit as a Git submodule:

```bash
# From the repository root
git submodule add https://github.com/your-org/cloud-ops-toolkit.git cloud-ops-toolkit
git submodule update --init

# Or set the path via environment variable
export CLOUD_OPS_TOOLKIT_PATH=../cloud-ops-toolkit
```

See [cloud-ops-toolkit/docs/integrations.md](../cloud-ops-toolkit/docs/integrations.md) for the full integration pattern documentation.

## Required IAM Permissions

The agent requires the following permissions (see `iam-policies/agent-execution-role.json`):

| Permission | Resource | Purpose |
|-----------|----------|---------|
| `bedrock:InvokeModel` | `arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-*` | Model inference |
| `bedrock:CreateAgent`, `bedrock:InvokeAgent` | `arn:aws:bedrock:us-east-1:123456789012:agent/*` | Agent management |
| `lambda:InvokeFunction` | `arn:aws:lambda:us-east-1:123456789012:function:demo-agents-*` | Action group execution |
| `ce:GetCostAndUsage` | `*` | Cost analysis |
| `tag:GetResources` | `*` | Resource listing |

> **Note:** All ARNs use placeholder account ID `123456789012`. Replace with your actual account ID before deployment.

## Setup

### Prerequisites

- Python 3.11+
- AWS CLI configured with a named profile
- AWS SAM CLI (for deployment)
- cloud-ops-toolkit cloned as submodule

### Installation

```bash
# Install dependencies for the Strands agent
cd strands-agent
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your AWS profile and region
```

### Local Testing (Strands Agent)

```bash
cd strands-agent
export AWS_PROFILE=your-profile-name
export AWS_REGION=us-east-1
python agent.py
```

## Deployment

### Deploy via SAM

```bash
cd infra

# Build the Lambda package
sam build

# Deploy (first time — guided)
sam deploy --guided

# Subsequent deployments
sam deploy --profile your-profile-name
```

### Configuration

Edit `infra/samconfig.toml` to customize:
- `stack_name` — CloudFormation stack name
- `region` — Target AWS region
- `profile` — AWS CLI profile
- `parameter_overrides` — Environment (dev/staging/prod)

## Cost Estimate

See [COST-ESTIMATE.md](./COST-ESTIMATE.md) for estimated AWS costs.

**Summary:** $5–25/month for demo-level usage (primarily Bedrock inference costs).

## Teardown

Remove all deployed AWS resources to stop incurring charges:

```bash
./teardown.sh
```

Or manually:

```bash
cd infra
sam delete --stack-name demo-agents-stack --profile your-profile-name --no-prompts
```

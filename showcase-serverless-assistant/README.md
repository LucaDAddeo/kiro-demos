# Serverless AI Assistant — End-to-End Showcase

> **Execution mode:** Deployable + Local dev  
> **Languages:** Python 3.11  
> **Kiro features:** Specs, Hooks, Steering

A complete serverless AI assistant that demonstrates how Kiro's spec-driven development, hooks, and steering files work together in a real-world AWS application.

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Client    │────▶│  API Gateway     │────▶│  Lambda (Chat)  │
│  (HTTP)     │◀────│  (HTTP API)      │◀────│                 │
└─────────────┘     └──────────────────┘     └────────┬────────┘
                                                       │
                              ┌─────────────────────────┼──────────────────┐
                              │                         │                  │
                              ▼                         ▼                  ▼
                    ┌─────────────────┐     ┌─────────────────┐  ┌──────────────┐
                    │   DynamoDB      │     │  Amazon Bedrock  │  │   Lambda     │
                    │ (Conversations) │     │  (Claude)        │  │  (History)   │
                    └─────────────────┘     └─────────────────┘  └──────────────┘
```

**Components:**

- **API Gateway (HTTP API)** — Routes requests to Lambda functions with CORS support
- **Lambda (Chat)** — Receives user messages, invokes Bedrock, stores conversations
- **Lambda (History)** — Retrieves conversation history by session ID
- **DynamoDB** — Stores conversation messages with session_id (PK) and timestamp (SK)
- **Amazon Bedrock** — Generates AI responses using Claude Sonnet

## Kiro Features Used

### Specs (`.kiro/specs/assistant-api/`)

The entire project was built following the Kiro spec workflow:

1. **requirements.md** — Defines API endpoints, data models, and behavior
2. **design.md** — Technical architecture, interfaces, and error handling
3. **tasks.md** — Implementation plan with task IDs referenced in source code

### Hooks (`.kiro/hooks/`)

- **test-on-save.json** — Automatically runs tests when Python files change (`fileEdited`)
- **security-check.json** — Validates write operations for security concerns (`preToolUse`)

### Steering (`.kiro/steering/`)

- **aws-best-practices.md** — Always-on guidance for AWS service usage (auto inclusion)
- **api-design.md** — Conditional guidance activated when editing API handler files

## Project Structure

```
showcase-serverless-assistant/
├── .kiro/                    # Kiro configuration
│   ├── specs/assistant-api/  # Full spec workflow artifacts
│   ├── hooks/                # Automation hooks
│   └── steering/             # Contextual guidance
├── src/
│   ├── handlers/             # Lambda function handlers
│   ├── core/                 # Business logic and models
│   └── utils/                # AWS helper utilities
├── tests/
│   ├── unit/                 # Unit tests for core logic
│   └── integration/          # Integration tests (mocked AWS)
├── infra/
│   ├── template.yaml         # SAM template
│   └── samconfig.toml        # SAM deployment config
├── local-dev.sh              # Local development script
├── teardown.sh               # AWS resource cleanup
└── COST-ESTIMATE.md          # Estimated AWS costs
```

## Local Development

### Prerequisites

- Python 3.11+
- AWS SAM CLI (`pip install aws-sam-cli`)
- Docker (for SAM local)

### Setup

```bash
cd showcase-serverless-assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Run Locally with SAM

```bash
# Start local API (requires Docker)
./local-dev.sh

# Or manually:
sam local start-api --template infra/template.yaml --port 3000
```

The local API will be available at `http://localhost:3000`.

**Test endpoints:**

```bash
# Send a chat message
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is serverless computing?"}'

# Get conversation history
curl http://localhost:3000/history/{session_id}
```

## AWS Deployment

### Prerequisites

- AWS CLI configured with appropriate credentials
- SAM CLI installed
- An AWS account with Bedrock model access enabled

### Deploy

```bash
cd infra

# Build the application
sam build

# Deploy (guided for first time)
sam deploy --guided

# Subsequent deployments
sam deploy
```

The deployment creates:
- HTTP API Gateway endpoint
- Two Lambda functions (chat + history)
- DynamoDB table (pay-per-request)
- IAM roles with least-privilege policies

### Configuration

Edit `infra/samconfig.toml` to customize:
- Stack name
- AWS region
- Environment (dev/staging/prod)

## Cost Estimate

See [COST-ESTIMATE.md](./COST-ESTIMATE.md) for detailed pricing breakdown.

**Summary (dev/test usage):** ~$1–5/month for light usage (< 1000 requests/day).

## Teardown

To remove all deployed AWS resources and avoid ongoing charges:

```bash
./teardown.sh
```

Or manually:

```bash
aws cloudformation delete-stack --stack-name assistant-dev
```

> **Important:** The DynamoDB table will be deleted along with all conversation data. Export any data you need before teardown.

## API Reference

### POST /chat

Send a message and receive an AI response.

**Request:**
```json
{
  "message": "Your question here",
  "session_id": "optional-existing-session-id"
}
```

**Response (200):**
```json
{
  "response": "AI-generated answer",
  "session_id": "uuid-session-id",
  "timestamp": "2024-01-01T00:00:00+00:00"
}
```

### GET /history/{session_id}

Retrieve conversation history for a session.

**Response (200):**
```json
{
  "session_id": "uuid-session-id",
  "messages": [
    {"role": "user", "content": "...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "timestamp": "..."}
  ]
}
```

## License

This project is part of the kiro-ambassador-demos repository for educational purposes.

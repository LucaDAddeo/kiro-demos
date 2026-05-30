# Design Document

## Overview

The serverless assistant API uses a two-Lambda architecture behind API Gateway, with DynamoDB for persistence and Amazon Bedrock for AI response generation.

## Architecture

```
Client → API Gateway → ChatFunction (Lambda) → Bedrock (Claude)
                    ↘                         ↘
                     HistoryFunction (Lambda) → DynamoDB (ConversationsTable)
```

## Components

### ChatFunction (Lambda)
- Receives POST /chat requests
- Validates input, generates session_id if missing
- Calls Bedrock via `create_response()` in core/assistant.py
- Stores user message and assistant response in DynamoDB
- Returns JSON response with session_id and timestamp

### HistoryFunction (Lambda)
- Receives GET /history/{session_id} requests
- Queries DynamoDB for all messages in the session
- Returns messages sorted by timestamp

### Core Business Logic (src/core/)
- `assistant.py`: Orchestrates Bedrock calls, formats prompts
- `models.py`: Dataclasses for ChatMessage, ChatResponse, ConversationHistory

### Utilities (src/utils/)
- `aws_helpers.py`: DynamoDB and Bedrock client initialization with environment-based configuration

## Data Model

### ConversationsTable (DynamoDB)
- Partition key: `session_id` (String)
- Sort key: `timestamp` (String, ISO 8601)
- Attributes: `role` (user|assistant), `content` (String)

## Error Handling

| Error | HTTP Status | Response |
|-------|-------------|----------|
| Missing message field | 400 | `{"error": "message is required"}` |
| Bedrock invocation failure | 502 | `{"error": "AI service unavailable"}` |
| DynamoDB write failure | 500 | `{"error": "Failed to save message"}` |
| Invalid session_id format | 400 | `{"error": "Invalid session_id"}` |

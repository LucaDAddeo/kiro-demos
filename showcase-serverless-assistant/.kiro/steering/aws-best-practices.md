---
inclusion: auto
description: "AWS serverless best practices applied to all project files"
---

# AWS Serverless Best Practices

## Lambda Functions
- Keep handlers thin: extract business logic into separate modules
- Use environment variables for all configuration (table names, model IDs, regions)
- Set appropriate memory and timeout values (start with 256MB, 30s timeout)
- Use structured logging with correlation IDs for traceability

## DynamoDB
- Design access patterns before creating tables
- Use partition key + sort key for efficient queries
- Prefer Query over Scan operations
- Use DynamoDB conditions for optimistic locking when needed

## API Gateway
- Validate request bodies at the API Gateway level when possible
- Use appropriate HTTP status codes (400 for client errors, 502 for upstream failures)
- Enable CORS only for required origins

## Security
- Never hardcode credentials — use IAM roles and environment variables
- Apply least-privilege IAM policies
- Validate and sanitize all input at the handler level
- Use AWS SDK default credential chain (no explicit key configuration)

## Error Handling
- Return structured error responses: `{"error": "message", "code": "ERROR_CODE"}`
- Log errors with full context but never log sensitive data
- Use try/except around all AWS SDK calls with specific exception handling

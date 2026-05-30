---
inclusion: conditional
globs: "**/*.py"
description: "AWS best practices applied when working with Python files that interact with AWS services"
---

# AWS Development Patterns

## Boto3 Session Management

- Always create explicit sessions rather than using the default session:
  ```python
  session = boto3.Session(profile_name="your-profile-name", region_name="us-east-1")
  client = session.client("s3")
  ```
- Pass sessions as parameters to functions for testability
- Never hardcode credentials; rely on credential chain (env vars, profiles, IAM roles)

## Pagination Handling

- Always use paginators for AWS API calls that return paginated results:
  ```python
  paginator = client.get_paginator("list_objects_v2")
  for page in paginator.paginate(Bucket="your-bucket-name"):
      for obj in page.get("Contents", []):
          process(obj)
  ```
- Never assume a single API call returns all results
- Set appropriate `MaxItems` or `PageSize` for performance

## Retry Logic

- Use botocore's built-in retry configuration:
  ```python
  from botocore.config import Config
  config = Config(retries={"max_attempts": 3, "mode": "adaptive"})
  client = session.client("dynamodb", config=config)
  ```
- Implement exponential backoff for custom retry logic
- Handle `ThrottlingException` and `TooManyRequestsException` gracefully

## Error Handling

- Catch specific AWS exceptions using client exceptions:
  ```python
  try:
      response = client.get_item(TableName="table", Key=key)
  except client.exceptions.ResourceNotFoundException:
      logger.warning("Table not found")
  except botocore.exceptions.ClientError as e:
      if e.response["Error"]["Code"] == "AccessDeniedException":
          logger.error("Insufficient permissions")
      raise
  ```

## Resource Cleanup

- Use context managers or try/finally for resources that need cleanup
- Tag all created resources with project and environment identifiers
- Include teardown scripts for any provisioned infrastructure

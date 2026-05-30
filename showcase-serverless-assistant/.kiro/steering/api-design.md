---
inclusion: conditional
globs: "src/handlers/**/*.py"
description: "API design guidelines applied when editing handler files"
---

# API Design Guidelines

## Request Handling
- Parse and validate request body early in the handler
- Return 400 with descriptive error messages for invalid input
- Use consistent JSON response structure across all endpoints

## Response Format
- Always return JSON with Content-Type: application/json
- Success responses include relevant data fields
- Error responses follow: `{"error": "Human-readable message", "code": "MACHINE_CODE"}`

## HTTP Status Codes
- 200: Successful retrieval or operation
- 201: Resource created (not used in this API)
- 400: Client error (missing fields, invalid format)
- 404: Resource not found (prefer 200 with empty result for collections)
- 500: Internal server error (DynamoDB failures)
- 502: Upstream service error (Bedrock failures)

## Lambda Handler Pattern
```python
def lambda_handler(event, context):
    try:
        # 1. Parse input
        body = json.loads(event.get("body", "{}"))
        
        # 2. Validate input
        if not body.get("required_field"):
            return {"statusCode": 400, "body": json.dumps({"error": "..."})}
        
        # 3. Execute business logic (delegate to core/)
        result = core_function(validated_input)
        
        # 4. Return success response
        return {"statusCode": 200, "body": json.dumps(result)}
    except SpecificException as e:
        return {"statusCode": appropriate_code, "body": json.dumps({"error": str(e)})}
```

## Path Parameters
- Extract from `event["pathParameters"]["param_name"]`
- Validate format before using in queries

## CORS
- Include Access-Control-Allow-Origin in responses
- Keep allowed origins restrictive (configure via environment variable)

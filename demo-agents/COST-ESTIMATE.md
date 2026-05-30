# Cost Estimate

## Services Used
- AWS Lambda: ~$0.20/million requests
- Amazon Bedrock (Claude): ~$3.00/million input tokens, ~$15.00/million output tokens
- Amazon DynamoDB (optional): ~$1.25/million write requests

## Estimated Monthly Cost (light demo usage)
- Lambda invocations: < $1.00
- Bedrock inference: $5-20 (depends on usage)
- Total: **$5-25/month** for demo purposes

## Teardown
Run `./teardown.sh` to delete all deployed resources and stop incurring charges.

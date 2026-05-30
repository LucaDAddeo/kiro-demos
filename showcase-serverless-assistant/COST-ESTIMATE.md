# Cost Estimate — Serverless AI Assistant

Estimated monthly AWS costs for the Serverless AI Assistant showcase project.

> **Note:** All prices are approximate and based on us-east-1 region pricing as of 2024. Actual costs may vary based on usage patterns and AWS pricing changes.

## Components

### Amazon API Gateway (HTTP API)

| Metric | Estimate |
|--------|----------|
| Requests/month | 30,000 (dev/test) |
| Price per million requests | $1.00 |
| **Monthly cost** | **~$0.03** |

### AWS Lambda

| Metric | Estimate |
|--------|----------|
| Invocations/month | 30,000 |
| Avg duration (chat) | 3,000 ms |
| Avg duration (history) | 200 ms |
| Memory | 256 MB |
| **Monthly cost** | **~$0.50** |

> Lambda free tier includes 1M requests and 400,000 GB-seconds/month.

### Amazon DynamoDB (On-Demand)

| Metric | Estimate |
|--------|----------|
| Write requests/month | 60,000 (2 per chat) |
| Read requests/month | 30,000 |
| Storage | < 1 GB |
| **Monthly cost** | **~$0.10** |

> DynamoDB free tier includes 25 GB storage and 25 WCU/RCU provisioned.

### Amazon Bedrock (Claude Sonnet)

| Metric | Estimate |
|--------|----------|
| Input tokens/month | 3M (~100 tokens/request) |
| Output tokens/month | 6M (~200 tokens/response) |
| Input price per 1K tokens | $0.003 |
| Output price per 1K tokens | $0.015 |
| **Monthly cost** | **~$1.00–4.00** |

> Bedrock pricing varies by model. Claude Sonnet pricing shown above.

## Total Estimated Cost

| Usage Level | Monthly Cost |
|-------------|-------------|
| Dev/Test (< 1,000 req/day) | **$1–5** |
| Light production (5,000 req/day) | **$15–30** |
| Moderate production (20,000 req/day) | **$60–120** |

## Cost Optimization Tips

1. **Use Lambda free tier** — First 1M requests/month are free
2. **Enable DynamoDB TTL** — Auto-delete old conversations to reduce storage
3. **Set Bedrock max_tokens** — Limit response length to control token costs
4. **Use API Gateway throttling** — Prevent unexpected cost spikes
5. **Deploy in a single region** — Avoid cross-region data transfer charges

## Teardown

To stop all charges immediately:

```bash
./teardown.sh
```

This deletes the CloudFormation stack and all associated resources. DynamoDB data will be permanently lost.

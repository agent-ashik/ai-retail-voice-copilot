# AWS Deployment Guide

## Prerequisites

- AWS Account with credits
- AWS CLI configured (`aws configure`)
- Docker installed
- Python 3.11+

## Quick Start - Local Development

1. **Clone and setup:**
```bash
git clone https://github.com/agent-ashik/ai-retail-voice-copilot.git
cd ai-retail-voice-copilot
```

2. **Start with Docker Compose:**
```bash
docker-compose up -d
```

3. **Access the application:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## AWS Deployment

### Step 1: Prepare AWS Resources

#### 1.1 Create RDS PostgreSQL Database

```bash
aws rds create-db-instance \
    --db-instance-identifier voice-copilot-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.3 \
    --master-username voicecopilot \
    --master-user-password YOUR_SECURE_PASSWORD \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-YOUR_SECURITY_GROUP \
    --db-subnet-group-name your-db-subnet-group \
    --publicly-accessible false \
    --region us-east-1
```

#### 1.2 Create ElastiCache Redis Cluster

```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id voice-copilot-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1 \
    --security-group-ids sg-YOUR_SECURITY_GROUP \
    --cache-subnet-group-name your-cache-subnet-group \
    --region us-east-1
```

#### 1.3 Store Secrets in AWS Secrets Manager

```bash
# Database URL
aws secretsmanager create-secret \
    --name voice-copilot/database-url \
    --secret-string "postgresql://voicecopilot:YOUR_PASSWORD@your-rds-endpoint:5432/retail_voice_copilot" \
    --region us-east-1

# Redis URL
aws secretsmanager create-secret \
    --name voice-copilot/redis-url \
    --secret-string "redis://your-redis-endpoint:6379/0" \
    --region us-east-1

# JWT Secret
aws secretsmanager create-secret \
    --name voice-copilot/jwt-secret \
    --secret-string "$(openssl rand -base64 32)" \
    --region us-east-1
```

### Step 2: Deploy to ECS

#### 2.1 Build and Push Docker Image

```bash
chmod +x aws/deploy.sh
./aws/deploy.sh
```

#### 2.2 Create ECS Task Definition

Update `aws/task-definition.json` with your AWS account ID and resource ARNs, then:

```bash
aws ecs register-task-definition \
    --cli-input-json file://aws/task-definition.json \
    --region us-east-1
```

#### 2.3 Create ECS Service

```bash
aws ecs create-service \
    --cluster ai-retail-voice-copilot-cluster \
    --service-name ai-retail-voice-copilot-service \
    --task-definition ai-retail-voice-copilot-task \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:xxx:targetgroup/xxx,containerName=voice-copilot-app,containerPort=8000" \
    --region us-east-1
```

### Step 3: Configure Application Load Balancer

#### 3.1 Create ALB

```bash
aws elbv2 create-load-balancer \
    --name voice-copilot-alb \
    --subnets subnet-xxx subnet-yyy \
    --security-groups sg-xxx \
    --region us-east-1
```

#### 3.2 Create Target Group

```bash
aws elbv2 create-target-group \
    --name voice-copilot-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id vpc-xxx \
    --target-type ip \
    --health-check-path /health \
    --region us-east-1
```

#### 3.3 Create Listener

```bash
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:xxx:loadbalancer/app/voice-copilot-alb/xxx \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:xxx:targetgroup/voice-copilot-tg/xxx \
    --region us-east-1
```

### Step 4: Configure AWS Services for Voice

#### 4.1 Enable AWS Transcribe

No setup required - service is pay-per-use.

#### 4.2 Enable AWS Polly

No setup required - service is pay-per-use.

#### 4.3 Create AWS Lex Bot (Optional for MVP)

```bash
# Create bot via AWS Console or CLI
# Bot name: retail-voice-copilot
# Languages: en_US, hi_IN, ta_IN, bn_IN
```

#### 4.4 Create S3 Bucket for Voice Recordings

```bash
aws s3 mb s3://voice-copilot-recordings-YOUR_ACCOUNT_ID --region us-east-1

# Configure lifecycle policy for 30-day retention
aws s3api put-bucket-lifecycle-configuration \
    --bucket voice-copilot-recordings-YOUR_ACCOUNT_ID \
    --lifecycle-configuration file://aws/s3-lifecycle.json
```

## Testing the Deployment

### Test Health Endpoint

```bash
curl http://your-alb-dns-name/health
```

### Test Stockout Prediction

```bash
curl -X POST http://your-alb-dns-name/api/v1/query/stockout \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "STORE-001",
    "days_ahead": 7
  }'
```

### Test Overstock Detection

```bash
curl -X POST http://your-alb-dns-name/api/v1/query/overstock \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "STORE-001"
  }'
```

### Test Replenishment Suggestions

```bash
curl -X POST http://your-alb-dns-name/api/v1/query/replenishment \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "STORE-001",
    "budget_limit": 50000
  }'
```

## Monitoring

### CloudWatch Logs

```bash
aws logs tail /ecs/ai-retail-voice-copilot --follow --region us-east-1
```

### CloudWatch Metrics

Monitor in AWS Console:
- ECS Service CPU/Memory utilization
- ALB request count and latency
- RDS connections and performance
- ElastiCache hit rate

## Cost Estimation

### Monthly costs for 100 stores (50 queries/store/day):

- **ECS Fargate** (2 tasks, 0.5 vCPU, 1GB): ~$30
- **RDS PostgreSQL** (db.t3.micro): ~$15
- **ElastiCache Redis** (cache.t3.micro): ~$12
- **ALB**: ~$20
- **AWS Transcribe**: ~$2,000 (40,000 minutes)
- **AWS Polly**: ~$800 (20M characters)
- **S3 + Data Transfer**: ~$50
- **CloudWatch**: ~$10

**Total: ~$2,937/month** (~$29/store/month)

## Scaling

### Auto Scaling

```bash
aws application-autoscaling register-scalable-target \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/ai-retail-voice-copilot-cluster/ai-retail-voice-copilot-service \
    --min-capacity 2 \
    --max-capacity 10 \
    --region us-east-1
```

## Troubleshooting

### Check ECS Task Logs

```bash
aws ecs describe-tasks \
    --cluster ai-retail-voice-copilot-cluster \
    --tasks TASK_ID \
    --region us-east-1
```

### Check Service Events

```bash
aws ecs describe-services \
    --cluster ai-retail-voice-copilot-cluster \
    --services ai-retail-voice-copilot-service \
    --region us-east-1
```

## Security Best Practices

1. Use AWS Secrets Manager for all sensitive data
2. Enable VPC endpoints for AWS services
3. Use security groups to restrict access
4. Enable CloudTrail for audit logging
5. Rotate JWT secrets regularly
6. Use HTTPS with ACM certificates
7. Enable WAF for API protection

## Next Steps

1. Implement authentication (JWT tokens)
2. Add AWS Transcribe/Polly integration
3. Implement AWS Lex for intent parsing
4. Add real forecasting models (Prophet/ARIMA)
5. Implement property-based tests
6. Set up CI/CD pipeline
7. Add monitoring dashboards
8. Implement rate limiting
9. Add API documentation
10. Create admin dashboard

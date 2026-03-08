#!/bin/bash
# AWS Deployment Script for AI Retail Voice Copilot

set -e

echo "🚀 Starting AWS deployment..."

# Configuration
APP_NAME="ai-retail-voice-copilot"
AWS_REGION="${AWS_REGION:-us-east-1}"
ECR_REPOSITORY="${APP_NAME}"
ECS_CLUSTER="${APP_NAME}-cluster"
ECS_SERVICE="${APP_NAME}-service"
TASK_FAMILY="${APP_NAME}-task"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Building Docker image...${NC}"
docker build -t ${APP_NAME}:latest .

echo -e "${YELLOW}Step 2: Creating ECR repository (if not exists)...${NC}"
aws ecr describe-repositories --repository-names ${ECR_REPOSITORY} --region ${AWS_REGION} || \
aws ecr create-repository --repository-name ${ECR_REPOSITORY} --region ${AWS_REGION}

echo -e "${YELLOW}Step 3: Getting ECR login...${NC}"
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.${AWS_REGION}.amazonaws.com

echo -e "${YELLOW}Step 4: Tagging and pushing image to ECR...${NC}"
ECR_URI=$(aws ecr describe-repositories --repository-names ${ECR_REPOSITORY} --region ${AWS_REGION} --query 'repositories[0].repositoryUri' --output text)
docker tag ${APP_NAME}:latest ${ECR_URI}:latest
docker push ${ECR_URI}:latest

echo -e "${YELLOW}Step 5: Creating ECS cluster (if not exists)...${NC}"
aws ecs describe-clusters --clusters ${ECS_CLUSTER} --region ${AWS_REGION} || \
aws ecs create-cluster --cluster-name ${ECS_CLUSTER} --region ${AWS_REGION}

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${GREEN}ECR Image: ${ECR_URI}:latest${NC}"
echo ""
echo "Next steps:"
echo "1. Create RDS PostgreSQL database"
echo "2. Create ElastiCache Redis cluster"
echo "3. Update task definition with database URLs"
echo "4. Create ECS service"
echo "5. Configure Application Load Balancer"

# Quick Start Guide

## Test the MVP Locally (5 minutes)

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Wait for services to be healthy (30 seconds)
docker-compose ps

# Test the API
curl http://localhost:8000/health
```

### Option 2: Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and set:
# DATABASE_URL=sqlite:///./test.db  # For quick testing
# JWT_SECRET_KEY=test-secret-key

# Run the application
python -m uvicorn src.voice_copilot.main:app --reload
```

## Test the API Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "AI Retail Voice Copilot",
  "version": "1.0.0"
}
```

### 2. Stockout Prediction
```bash
curl -X POST http://localhost:8000/api/v1/query/stockout \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "STORE-001",
    "days_ahead": 7
  }'
```

Expected response:
```json
{
  "success": true,
  "store_id": "STORE-001",
  "predictions_count": 3,
  "predictions": [
    {
      "sku": "SKU-003",
      "sku_name": "Sugar 1kg",
      "current_stock": 20,
      "predicted_stockout_date": "2026-03-12",
      "confidence": 0.88,
      "urgency_level": "HIGH"
    },
    ...
  ]
}
```

### 3. Overstock Detection
```bash
curl -X POST http://localhost:8000/api/v1/query/overstock \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "STORE-001"
  }'
```

Expected response:
```json
{
  "success": true,
  "store_id": "STORE-001",
  "overstocked_count": 3,
  "overstocked_items": [
    {
      "sku": "SKU-005",
      "sku_name": "Tea Bags 100ct",
      "current_stock": 800,
      "max_threshold": 300,
      "excess_quantity": 500,
      "excess_percentage": 166.67,
      "days_of_supply": 100.0
    },
    ...
  ]
}
```

### 4. Replenishment Suggestions
```bash
curl -X POST http://localhost:8000/api/v1/query/replenishment \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "STORE-001",
    "budget_limit": 50000
  }'
```

Expected response:
```json
{
  "success": true,
  "store_id": "STORE-001",
  "generated_date": "2026-03-08",
  "total_estimated_cost": 43400.0,
  "priority_level": "URGENT",
  "order_items_count": 3,
  "order_items": [
    {
      "sku": "SKU-001",
      "sku_name": "Basmati Rice 5kg",
      "suggested_quantity": 100,
      "unit_cost": 250.0,
      "total_cost": 25000.0,
      "urgency_level": "HIGH",
      "predicted_stockout_date": "2026-03-10",
      "current_stock": 50.0
    },
    ...
  ]
}
```

## Access API Documentation

Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## View Logs

### Docker Compose
```bash
# All services
docker-compose logs -f

# Just the app
docker-compose logs -f app
```

### Python
Logs will appear in the terminal where you ran uvicorn.

## Stop Services

### Docker Compose
```bash
docker-compose down
```

### Python
Press `Ctrl+C` in the terminal.

## Next Steps

1. **Deploy to AWS**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
2. **Add Real Data**: Connect to actual PostgreSQL database
3. **Integrate AWS Services**: Add Transcribe/Polly for voice
4. **Add Authentication**: Implement JWT tokens
5. **Run Tests**: `pytest tests/`

## Troubleshooting

### Port 8000 already in use
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

### Docker issues
```bash
# Clean up and restart
docker-compose down -v
docker-compose up -d --build
```

### Python dependency issues
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Demo Video Script

1. Start services: `docker-compose up -d`
2. Show health check: `curl http://localhost:8000/health`
3. Demo stockout prediction with explanation
4. Demo overstock detection with explanation
5. Demo replenishment suggestions with cost breakdown
6. Show API docs at http://localhost:8000/docs
7. Explain AWS deployment architecture

## Support

- GitHub Issues: https://github.com/agent-ashik/ai-retail-voice-copilot/issues
- Documentation: See README.md and DEPLOYMENT.md

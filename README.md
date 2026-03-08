# AI Retail Voice Operations Copilot

A multilingual voice-enabled assistant that empowers store managers to make data-driven inventory decisions through natural voice interactions in regional languages.

## Features

- **Voice-First Interface**: Natural language queries in English, Hindi, Tamil, and Bengali
- **Stockout Prediction**: AI-powered forecasting with 7-30 day horizon
- **Overstock Detection**: Identify excess inventory with configurable thresholds
- **Intelligent Replenishment**: EOQ-based order suggestions with constraints
- **Anomaly Detection**: Real-time inventory pattern analysis
- **Multi-Store Support**: Cross-store visibility with role-based access control

## Architecture

Built with:
- **Backend**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis
- **ML/AI**: Facebook Prophet, statsmodels
- **AWS Services**: Transcribe, Polly, Lex, RDS, ElastiCache, S3, Lambda
- **Testing**: pytest, hypothesis (property-based testing)

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 14+
- Redis 7+
- AWS Account with credits

### Installation

1. Clone the repository:
```bash
git clone https://github.com/agent-ashik/ai-retail-voice-copilot.git
cd ai-retail-voice-copilot
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the application:
```bash
uvicorn src.voice_copilot.main:app --reload
```

## Development

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest -m unit

# Property-based tests
pytest -m property

# With coverage
pytest --cov=src/voice_copilot --cov-report=html
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

## Project Structure

```
.
├── src/
│   └── voice_copilot/
│       ├── models/          # SQLAlchemy models
│       ├── services/        # Business logic
│       ├── api/             # FastAPI routes
│       └── utils/           # Utilities
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── property_based/     # Property-based tests
├── config/                 # Configuration files
├── scripts/                # Utility scripts
└── docs/                   # Documentation

```

## Documentation

- [Requirements](/.kiro/specs/ai-retail-voice-copilot/requirements.md)
- [Design](/.kiro/specs/ai-retail-voice-copilot/design.md)
- [Tasks](/.kiro/specs/ai-retail-voice-copilot/tasks.md)

## License

MIT License - see LICENSE file for details

## Team

VaniCommerce - AWS AI for Bharat Hackathon 2024

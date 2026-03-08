# Implementation Plan: AI Retail Voice Operations Copilot

## Overview

This implementation plan breaks down the AI Retail Voice Operations Copilot into discrete coding tasks. The system will be built using Python with a microservices architecture, integrating cloud-based speech services, time-series forecasting models, and inventory analytics. The implementation follows a bottom-up approach: core data models → analytics components → voice interface → orchestration → integration.

All property-based tests use the `hypothesis` library for Python and are configured to run a minimum of 100 iterations. Each property test references its corresponding design document property number.

## Tasks

- [-] 1. Set up project structure and core infrastructure
  - Create Python project with virtual environment (Python 3.9+)
  - Set up directory structure: `src/`, `tests/`, `config/`, `models/`, `scripts/`
  - Configure dependencies: FastAPI, SQLAlchemy, boto3 (AWS SDK), pytest, hypothesis, fast-check (for property tests)
  - Set up configuration management for environment variables (python-dotenv)
  - Create base exception classes and logging configuration (structlog)
  - Configure pytest with hypothesis plugin for property-based testing
  - _Requirements: 10.1, 10.2_

- [ ] 2. Implement core data models and database layer
  - [ ] 2.1 Create SQLAlchemy models for inventory, sales, forecasts, and users
    - Implement `InventoryRecord`, `SKUMaster`, `SalesTransaction`, `DailySalesSummary` models
    - Implement `ForecastRecord`, `StockoutPredictionRecord` models
    - Implement `User`, `Store` models with relationships
    - Add database indexes for query performance
    - _Requirements: 2.1, 3.1, 4.1, 8.1_
  
  - [ ]* 2.2 Write unit tests for data model validation
    - Test model field constraints and relationships
    - Test data integrity constraints
    - _Requirements: 2.1, 3.1, 4.1_
  
  - [ ] 2.3 Create database connection manager and repository pattern
    - Implement connection pooling and session management
    - Create repository classes for each model with CRUD operations
    - Add transaction management and rollback handling
    - _Requirements: 9.1, 10.1_
  
  - [ ]* 2.4 Write unit tests for repository operations
    - Test CRUD operations with in-memory SQLite
    - Test transaction rollback scenarios
    - Test connection error handling
    - _Requirements: 2.1, 3.1, 4.1_

- [ ] 3. Implement Forecasting Engine component
  - [ ] 3.1 Create forecasting model interface and base classes
    - Define abstract `ForecastingModel` base class with predict() and train() methods
    - Implement time-series data preprocessing utilities (normalization, missing value handling)
    - Create feature engineering functions (seasonality indicators, trend extraction, promotional flags)
    - _Requirements: 2.1, 2.2, 2.4_
  
  - [ ] 3.2 Implement demand forecasting using Prophet or ARIMA
    - Integrate Facebook Prophet (preferred) or statsmodels ARIMA for time-series forecasting
    - Implement model training pipeline with historical sales data (minimum 30 days)
    - Create prediction functions for future demand with configurable forecast horizon
    - Add confidence interval calculations (80% and 95% intervals)
    - Handle edge cases: insufficient data, zero sales periods, missing data points
    - _Requirements: 2.2, 2.4_
  
  - [ ] 3.3 Implement stockout prediction logic
    - Calculate days until stockout based on current stock and predicted demand
    - Classify urgency levels (HIGH/MEDIUM/LOW) based on days until stockout
    - Generate `StockoutPrediction` objects with dates and confidence
    - _Requirements: 2.2, 2.3, 2.5_
  
  - [ ]* 3.4 Write property test for stockout prediction completeness
    - **Property 5: Stockout prediction completeness**
    - For any stockout prediction query, all SKUs predicted to stock out within the specified time window should be included in the response
    - Use hypothesis to generate random inventory states and time windows
    - **Validates: Requirements 2.3**
  
  - [ ]* 3.5 Write property test for stockout urgency ordering
    - **Property 6: Stockout urgency ordering**
    - For any list of stockout predictions, items should be sorted by predicted stockout date in ascending order
    - Use hypothesis to generate random lists of stockout predictions
    - **Validates: Requirements 2.5**
  
  - [ ] 3.6 Implement forecast accuracy tracking
    - Create functions to compare predictions vs actual sales
    - Calculate MAPE, RMSE, and accuracy percentage metrics
    - Store accuracy metrics by SKU category and time period
    - _Requirements: 7.2, 7.4, 7.5_
  
  - [ ]* 3.7 Write property tests for accuracy metrics
    - **Property 7: Forecast accuracy metric calculation**
    - For any set of predictions and actual sales data, verify MAPE, RMSE, and accuracy percentage are calculated correctly
    - **Property 8: Low accuracy flagging**
    - For any SKU category with forecast accuracy below 75%, verify it is flagged for model review
    - **Property 9: Category-specific accuracy tracking**
    - For any product category and time period, verify separate accuracy metrics are maintained
    - Use hypothesis to generate random prediction/actual pairs
    - **Validates: Requirements 7.2, 7.4, 7.5**

- [ ] 4. Checkpoint - Ensure forecasting tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Inventory Analyzer component
  - [ ] 5.1 Create inventory analysis functions
    - Implement overstock detection with configurable threshold (default 1.5x)
    - Calculate excess quantity, excess percentage, and days of supply
    - Implement sorting by severity (excess percentage)
    - _Requirements: 3.1, 3.2, 3.3, 3.5_
  
  - [ ]* 5.2 Write property tests for overstock detection
    - **Property 10: Overstock classification threshold**
    - For any SKU where current stock exceeds 1.5x maximum threshold, verify it is classified as overstocked
    - **Property 11: Overstock metric completeness**
    - For any overstocked item, verify excess quantity, excess percentage, and days of supply are included
    - **Property 12: Overstock severity ordering**
    - For any list of overstocked items, verify they are sorted by excess percentage descending
    - Use hypothesis to generate random inventory states
    - **Validates: Requirements 3.2, 3.3, 3.5**
  
  - [ ] 5.3 Implement anomaly detection algorithms
    - Calculate rolling mean and standard deviation for inventory levels (30-day window)
    - Detect anomalies using Z-score method (threshold: >2 standard deviations)
    - Classify anomaly types based on pattern analysis:
      - SUDDEN_SPIKE: >2 std dev increase in single day
      - SUDDEN_DROP: >2 std dev decrease in single day
      - GRADUAL_DRIFT: Sustained deviation over 7+ days
      - MISSING_DATA: Gaps in inventory records
    - Calculate severity: HIGH (>3 std devs), MEDIUM (2-3 std devs), LOW (<2 std devs)
    - _Requirements: 6.1, 6.2, 6.5_
  
  - [ ]* 5.4 Write property tests for anomaly detection
    - **Property 13: Anomaly detection threshold**
    - For any inventory data point deviating >2 standard deviations, verify it is flagged as an anomaly
    - **Property 14: Anomaly type classification**
    - For any detected anomaly, verify it is classified as SUDDEN_SPIKE, SUDDEN_DROP, GRADUAL_DRIFT, or MISSING_DATA
    - **Property 15: Anomaly information inclusion**
    - For any query about a SKU with anomalies, verify anomaly information is included in response
    - **Property 16: Anomaly prioritization**
    - For any list of anomalies, verify high-value SKUs and severe deviations are ranked higher
    - Use hypothesis to generate random inventory time series with injected anomalies
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.5**
  
  - [ ] 5.5 Implement inventory metrics calculator
    - Calculate average daily sales, days of supply, turnover rate
    - Determine reorder points based on lead time and safety stock
    - _Requirements: 3.3, 4.2_

- [ ] 6. Implement Replenishment Agent component
  - [ ] 6.1 Create replenishment suggestion engine
    - Identify SKUs below reorder point using current stock and lead time
    - Calculate optimal order quantities using Economic Order Quantity (EOQ) formula
    - Apply constraints: minimum order quantities (MOQ), budget limits, supplier lead times
    - Generate `ReplenishmentSuggestion` with complete order items including cost estimates
    - Handle edge cases: zero demand, infinite lead times, budget exhaustion
    - _Requirements: 4.1, 4.2, 4.3, 4.5, 4.6_
  
  - [ ] 6.2 Implement order prioritization logic
    - Sort order items by predicted stockout date in ascending order (earliest first)
    - Assign urgency levels: HIGH (<3 days), MEDIUM (3-7 days), LOW (>7 days)
    - Break ties by SKU value (higher value items prioritized)
    - _Requirements: 4.4_
  
  - [ ]* 6.3 Write property tests for replenishment logic
    - **Property 17: Replenishment calculation for low stock**
    - For any SKU below reorder point, verify an order quantity is calculated and included
    - **Property 18: Replenishment urgency ordering**
    - For any replenishment suggestion with multiple items, verify they are sorted by stockout date ascending
    - **Property 19: Replenishment quantity bounds**
    - For any suggested order quantity, verify resulting inventory is between min and max thresholds
    - **Property 20: Replenishment response completeness**
    - For any order item, verify it includes SKU, quantity, cost, and urgency level
    - Use hypothesis to generate random inventory states and constraints
    - **Validates: Requirements 4.2, 4.4, 4.5, 4.6**
  
  - [ ]* 6.4 Write unit tests for constraint handling
    - Test MOQ constraints
    - Test budget limit enforcement
    - Test lead time calculations
    - _Requirements: 4.3, 4.5_

- [ ] 7. Checkpoint - Ensure analytics components tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement Voice Interface component
  - [ ] 8.1 Create speech-to-text integration
    - Integrate AWS Transcribe or Google Speech-to-Text API with streaming support
    - Implement audio buffer handling for various formats (WAV, MP3, OGG)
    - Add automatic language detection using acoustic models (support: en, hi, ta, bn)
    - Return transcription with confidence scores and alternative transcriptions
    - Implement retry logic for transient API failures
    - _Requirements: 1.1, 1.2_
  
  - [ ] 8.2 Implement text-to-speech integration
    - Integrate AWS Polly or Google Text-to-Speech API
    - Support multiple languages (en, hi, ta, bn) with appropriate voice profiles
    - Implement response audio caching with Redis (TTL: 24 hours) for common responses
    - Add audio format conversion (MP3, OGG) based on client capabilities
    - _Requirements: 5.1_
  
  - [ ] 8.3 Create audio quality validation
    - Calculate signal-to-noise ratio (SNR) from audio samples
    - Validate audio format, sample rate (minimum 16kHz), and bit depth
    - Reject poor quality audio (SNR < 10dB) with user-friendly error messages
    - Detect and handle silent or empty audio files
    - _Requirements: 1.1, 1.4_
  
  - [ ]* 8.4 Write property tests for voice interface
    - **Property 1: Transcription accuracy threshold**
    - For any audio input in supported language with acceptable quality, verify confidence score ≥ 0.90
    - **Property 2: Language round-trip consistency**
    - For any voice query, verify detected language matches query language and response is synthesized in same language
    - **Property 4: Low confidence retry request**
    - For any audio with transcription confidence < 0.70, verify system requests user to repeat
    - Use hypothesis to generate mock audio inputs with varying quality and languages
    - **Validates: Requirements 1.1, 1.2, 1.4, 5.1**
  
  - [ ]* 8.5 Write unit tests for audio handling
    - Test audio format validation
    - Test error handling for API failures
    - Test caching behavior
    - _Requirements: 1.1, 1.2, 5.1_

- [ ] 9. Implement Intent Parser component
  - [ ] 9.1 Create NLU integration for intent classification
    - Integrate AWS Lex, Dialogflow, or Rasa NLU for intent recognition
    - Define intents with training phrases:
      - STOCKOUT_PREDICTION: "which items will run out", "stockout forecast"
      - OVERSTOCK_DETECTION: "overstocked items", "excess inventory"
      - REPLENISHMENT_SUGGESTION: "what should I order", "replenishment plan"
      - ANOMALY_QUERY: "unusual inventory", "inventory anomalies"
    - Train models with retail-specific vocabulary in all supported languages
    - _Requirements: 1.3_
  
  - [ ] 9.2 Implement parameter extraction logic
    - Extract time windows: parse "next 7 days", "this week", specific date ranges
    - Extract SKU filters: parse SKU codes, product names, categories
    - Extract store identifiers: parse store names, IDs, "all stores"
    - Handle missing parameters with intelligent defaults (e.g., 7-day window, primary store)
    - Implement slot filling for incomplete queries with clarification prompts
    - _Requirements: 1.3_
  
  - [ ]* 9.3 Write property test for parameter extraction
    - **Property 3: Intent parameter extraction completeness**
    - For any valid query text containing time ranges, SKU filters, or thresholds, verify all parameters are extracted correctly
    - Use hypothesis to generate random query texts with various parameter combinations
    - **Validates: Requirements 1.3**
  
  - [ ]* 9.4 Write unit tests for intent parsing
    - Test each intent type with example queries
    - Test multilingual queries
    - Test malformed queries
    - _Requirements: 1.3_

- [ ] 10. Implement Response Formatter component
  - [ ] 10.1 Create response formatting functions
    - Format stockout predictions: "5 items will stock out soon. Top item: [SKU] on [date]"
    - Format overstock items: "3 items are overstocked. [SKU] has 150% excess inventory"
    - Format replenishment suggestions: "Order [quantity] units of [SKU], estimated cost [amount]"
    - Truncate lists to top 5 items for voice delivery, offer full results via text/email
    - Add contextual information: data freshness, confidence levels
    - _Requirements: 5.2_
  
  - [ ] 10.2 Implement numerical formatting for speech
    - Convert numbers to natural spoken format: "1200" → "one thousand two hundred"
    - Format dates conversationally: "2024-03-15" → "March fifteenth"
    - Format currency with proper locale: "$1,234.56" → "one thousand two hundred thirty four dollars"
    - Handle large numbers with appropriate units: "1,000,000" → "one million"
    - _Requirements: 5.3_
  
  - [ ]* 10.3 Write property tests for response formatting
    - **Property 21: Voice response list truncation**
    - For any response with >5 items, verify only top 5 are included in voice output with offer to send full results
    - **Property 22: Numerical formatting for speech**
    - For any response with numerical values, verify they are formatted in natural spoken format
    - **Property 23: Long response alternative delivery**
    - For any response taking >30 seconds to speak, verify system offers text/email alternative
    - Use hypothesis to generate random response data with varying sizes and content
    - **Validates: Requirements 5.2, 5.3, 5.5**

- [ ] 11. Implement Query Orchestrator component
  - [ ] 11.1 Create query routing logic
    - Route STOCKOUT_PREDICTION queries to Forecasting Engine with time window parameters
    - Route OVERSTOCK_DETECTION queries to Inventory Analyzer with threshold parameters
    - Route REPLENISHMENT_SUGGESTION queries to Replenishment Agent with budget constraints
    - Route ANOMALY_QUERY queries to Inventory Analyzer for anomaly detection
    - Handle query errors gracefully: log errors, return user-friendly messages, aggregate partial results
    - Implement timeout handling (5 second timeout per component call)
    - _Requirements: 2.1, 3.1, 4.1, 6.3_
  
  - [ ] 11.2 Implement multi-store query handling
    - Apply store filters to database queries when store IDs specified
    - Default to user's primary assigned store when no store specified in query
    - Aggregate results across multiple stores, labeling each result with store identifier
    - Handle cross-store analytics: compare metrics, identify best/worst performing stores
    - _Requirements: 8.1, 8.2, 8.3_
  
  - [ ] 11.3 Implement access control enforcement
    - Validate user JWT token before processing any queries
    - Check user's authorized store list against requested store IDs
    - Reject unauthorized queries with HTTP 403 and descriptive error message
    - Log all authorization failures for security monitoring
    - _Requirements: 8.4, 9.3_
  
  - [ ]* 11.4 Write property tests for orchestrator logic
    - **Property 24: Store filter application**
    - For any query with store identifier filters, verify results only include data from specified stores
    - **Property 25: Default store assignment**
    - For any query without store identifier, verify user's primary assigned store is used
    - **Property 26: Multi-store result aggregation**
    - For any query spanning multiple stores, verify each result item is labeled with store identifier
    - **Property 27: Store access control enforcement**
    - For any query requesting unauthorized stores, verify it is rejected with authorization error
    - Use hypothesis to generate random queries with various store configurations
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 9.3**
  
  - [ ]* 11.5 Write unit tests for query routing
    - Test routing for each intent type
    - Test error aggregation
    - Test timeout handling
    - _Requirements: 2.1, 3.1, 4.1_

- [ ] 12. Checkpoint - Ensure orchestration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 13. Implement security and audit features
  - [ ] 13.1 Create authentication and authorization middleware
    - Implement JWT token validation using PyJWT library
    - Create role-based access control (RBAC): STORE_MANAGER, REGIONAL_MANAGER, ADMIN roles
    - Add authentication middleware to all protected API endpoints
    - Implement token refresh mechanism with secure refresh tokens
    - _Requirements: 9.3, 8.4_
  
  - [ ] 13.2 Implement audit logging
    - Log all queries with structured format: user_id, timestamp, query_type, store_id, intent, execution_time
    - Use structlog for structured JSON logging with correlation IDs
    - Implement log rotation: daily rotation, 90-day retention
    - Create audit log query API for administrators
    - _Requirements: 9.4_
  
  - [ ] 13.3 Implement voice recording retention policy
    - Store voice recordings with 30-day TTL
    - Create background job to delete expired recordings
    - Add metadata tracking for recording age
    - _Requirements: 9.2_
  
  - [ ]* 13.4 Write property tests for security features
    - **Property 28: Voice recording retention limit**
    - For any voice recording older than 30 days, verify it is automatically deleted
    - **Property 29: Query audit logging**
    - For any processed query, verify audit log entry contains user_id, timestamp, query_type, and store_id
    - Use hypothesis to generate random timestamps and query data
    - **Validates: Requirements 9.2, 9.4**

- [ ] 14. Implement caching and resilience features
  - [ ] 14.1 Create forecast cache layer
    - Implement Redis or in-memory cache for forecast results
    - Set TTL to 24 hours for forecast data
    - Add cache invalidation on data updates
    - _Requirements: 10.5_
  
  - [ ] 14.2 Implement request queueing for high load
    - Create request queue with capacity limits
    - Calculate and return estimated wait times
    - Process queued requests in FIFO order
    - _Requirements: 10.3_
  
  - [ ] 14.3 Implement fallback to cached data
    - Detect backend service unavailability
    - Return cached forecast data with staleness indicator
    - Add warnings about data freshness in responses
    - _Requirements: 10.5_
  
  - [ ]* 14.4 Write property tests for resilience features
    - **Property 30: Request queueing under load**
    - For any query submitted when system is at capacity, verify it is queued with estimated wait time
    - **Property 31: Cached data fallback**
    - For any query when backend services unavailable, verify cached forecast data is returned with staleness indicator
    - Use hypothesis to generate random load scenarios and service availability states
    - **Validates: Requirements 10.3, 10.5**

- [ ] 15. Implement FastAPI REST endpoints
  - [ ] 15.1 Create API endpoint for voice query processing
    - POST `/api/v1/query/voice` - accepts audio file, returns audio response
    - Integrate Voice Interface for transcription and synthesis
    - Call Intent Parser and Query Orchestrator
    - Return structured response with audio
    - _Requirements: 1.1, 1.2, 5.1, 10.1_
  
  - [ ] 15.2 Create API endpoints for direct queries (non-voice)
    - POST `/api/v1/query/stockout` - stockout predictions
    - POST `/api/v1/query/overstock` - overstock detection
    - POST `/api/v1/query/replenishment` - replenishment suggestions
    - Add request validation and error handling
    - _Requirements: 2.1, 3.1, 4.1_
  
  - [ ] 15.3 Create health check and metrics endpoints
    - GET `/health` - service health status
    - GET `/metrics` - Prometheus-compatible metrics
    - Add database connectivity checks
    - _Requirements: 10.2_
  
  - [ ]* 15.4 Write integration tests for API endpoints
    - Test end-to-end voice query flow
    - Test each direct query endpoint
    - Test authentication and authorization
    - Test error responses
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 9.3, 10.1_

- [ ] 16. Implement background jobs and scheduled tasks
  - [ ] 16.1 Create forecast update job
    - Schedule daily forecast updates for all stores
    - Fetch latest inventory and sales data
    - Run forecasting models and update cache
    - Log update status and errors
    - _Requirements: 2.6_
  
  - [ ] 16.2 Create anomaly detection job
    - Schedule anomaly detection every 6 hours
    - Analyze inventory data for all active SKUs
    - Store detected anomalies in database
    - Send alerts for high-severity anomalies
    - _Requirements: 6.4_
  
  - [ ] 16.3 Create model retraining job
    - Schedule monthly model retraining
    - Fetch recent historical data (last 12 months)
    - Retrain forecasting models
    - Validate model accuracy before deployment
    - _Requirements: 7.3_

- [ ] 17. Create deployment configuration and documentation
  - [ ] 17.1 Create Docker configuration
    - Write Dockerfile for Python application
    - Create docker-compose.yml for local development
    - Include PostgreSQL, Redis, and application services
    - _Requirements: 10.2_
  
  - [ ] 17.2 Create environment configuration templates
    - Document required environment variables
    - Create `.env.example` with all configuration options
    - Document cloud service credentials (AWS, GCP)
    - _Requirements: 9.1_
  
  - [ ] 17.3 Write API documentation
    - Document all REST endpoints with request/response examples
    - Create OpenAPI/Swagger specification
    - Document authentication requirements
    - Document supported languages and voice profiles
    - _Requirements: 1.5, 5.1_

- [ ] 18. Final checkpoint - Integration testing and validation
  - Run all unit tests and property tests
  - Perform end-to-end integration testing
  - Validate all requirements are met
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional property-based tests that can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation throughout development
- All property tests use the `hypothesis` library and run minimum 100 iterations
- Each property test includes a comment tag: `# Feature: ai-retail-voice-copilot, Property {N}: {description}`
- Property tests validate universal correctness properties across randomized inputs
- Unit tests validate specific examples, edge cases, and integration points
- The implementation uses Python with FastAPI, SQLAlchemy, and cloud-based speech services (AWS Transcribe/Polly or Google Speech APIs)
- Background jobs use APScheduler or Celery for task scheduling
- Caching uses Redis for distributed caching across instances
- All 31 correctness properties from the design document are mapped to property-based test tasks

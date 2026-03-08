"""
Configuration management for the Voice Copilot application.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="AI Retail Voice Copilot", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # Database
    database_url: str = Field(alias="DATABASE_URL")
    database_pool_size: int = Field(default=20, alias="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=10, alias="DATABASE_MAX_OVERFLOW")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    redis_ttl: int = Field(default=86400, alias="REDIS_TTL")
    
    # AWS
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    
    # AWS Transcribe
    aws_transcribe_language_codes: str = Field(
        default="en-US,hi-IN,ta-IN,bn-IN",
        alias="AWS_TRANSCRIBE_LANGUAGE_CODES"
    )
    
    # AWS Polly
    aws_polly_voice_en: str = Field(default="Joanna", alias="AWS_POLLY_VOICE_EN")
    aws_polly_voice_hi: str = Field(default="Aditi", alias="AWS_POLLY_VOICE_HI")
    aws_polly_voice_ta: str = Field(default="Aditi", alias="AWS_POLLY_VOICE_TA")
    aws_polly_voice_bn: str = Field(default="Aditi", alias="AWS_POLLY_VOICE_BN")
    
    # AWS Lex
    aws_lex_bot_id: Optional[str] = Field(default=None, alias="AWS_LEX_BOT_ID")
    aws_lex_bot_alias_id: Optional[str] = Field(default=None, alias="AWS_LEX_BOT_ALIAS_ID")
    aws_lex_locale_id: str = Field(default="en_US", alias="AWS_LEX_LOCALE_ID")
    
    # S3
    aws_s3_bucket: str = Field(default="retail-voice-recordings", alias="AWS_S3_BUCKET")
    aws_s3_recording_ttl_days: int = Field(default=30, alias="AWS_S3_RECORDING_TTL_DAYS")
    
    # JWT
    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, alias="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Forecasting
    forecast_horizon_days: int = Field(default=30, alias="FORECAST_HORIZON_DAYS")
    forecast_min_history_days: int = Field(default=30, alias="FORECAST_MIN_HISTORY_DAYS")
    forecast_cache_ttl_hours: int = Field(default=24, alias="FORECAST_CACHE_TTL_HOURS")
    
    # Inventory
    overstock_threshold_multiplier: float = Field(default=1.5, alias="OVERSTOCK_THRESHOLD_MULTIPLIER")
    anomaly_detection_std_dev_threshold: float = Field(default=2.0, alias="ANOMALY_DETECTION_STD_DEV_THRESHOLD")
    anomaly_detection_window_days: int = Field(default=30, alias="ANOMALY_DETECTION_WINDOW_DAYS")
    
    # Replenishment
    replenishment_urgency_high_days: int = Field(default=3, alias="REPLENISHMENT_URGENCY_HIGH_DAYS")
    replenishment_urgency_medium_days: int = Field(default=7, alias="REPLENISHMENT_URGENCY_MEDIUM_DAYS")
    
    # Performance
    query_timeout_seconds: int = Field(default=5, alias="QUERY_TIMEOUT_SECONDS")
    max_concurrent_requests: int = Field(default=100, alias="MAX_CONCURRENT_REQUESTS")
    request_queue_size: int = Field(default=500, alias="REQUEST_QUEUE_SIZE")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, alias="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, alias="METRICS_PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

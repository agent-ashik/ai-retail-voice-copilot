"""
Custom exception classes for the Voice Copilot application.
"""


class VoiceCopilotException(Exception):
    """Base exception for all Voice Copilot errors."""
    
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DatabaseException(VoiceCopilotException):
    """Exception raised for database-related errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="DATABASE_ERROR")


class ConfigurationException(VoiceCopilotException):
    """Exception raised for configuration errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="CONFIGURATION_ERROR")


class VoiceProcessingException(VoiceCopilotException):
    """Exception raised for voice processing errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="VOICE_PROCESSING_ERROR")


class TranscriptionException(VoiceProcessingException):
    """Exception raised for speech-to-text errors."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.code = "TRANSCRIPTION_ERROR"


class SynthesisException(VoiceProcessingException):
    """Exception raised for text-to-speech errors."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.code = "SYNTHESIS_ERROR"


class AudioQualityException(VoiceProcessingException):
    """Exception raised for poor audio quality."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.code = "AUDIO_QUALITY_ERROR"


class IntentParsingException(VoiceCopilotException):
    """Exception raised for intent parsing errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="INTENT_PARSING_ERROR")


class ForecastingException(VoiceCopilotException):
    """Exception raised for forecasting errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="FORECASTING_ERROR")


class InsufficientDataException(ForecastingException):
    """Exception raised when insufficient historical data is available."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.code = "INSUFFICIENT_DATA"


class InventoryAnalysisException(VoiceCopilotException):
    """Exception raised for inventory analysis errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="INVENTORY_ANALYSIS_ERROR")


class ReplenishmentException(VoiceCopilotException):
    """Exception raised for replenishment calculation errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="REPLENISHMENT_ERROR")


class AuthenticationException(VoiceCopilotException):
    """Exception raised for authentication errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="AUTHENTICATION_ERROR")


class AuthorizationException(VoiceCopilotException):
    """Exception raised for authorization errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="AUTHORIZATION_ERROR")


class ValidationException(VoiceCopilotException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class ServiceUnavailableException(VoiceCopilotException):
    """Exception raised when a service is unavailable."""
    
    def __init__(self, message: str):
        super().__init__(message, code="SERVICE_UNAVAILABLE")


class TimeoutException(VoiceCopilotException):
    """Exception raised when an operation times out."""
    
    def __init__(self, message: str):
        super().__init__(message, code="TIMEOUT_ERROR")


class CacheException(VoiceCopilotException):
    """Exception raised for caching errors."""
    
    def __init__(self, message: str):
        super().__init__(message, code="CACHE_ERROR")

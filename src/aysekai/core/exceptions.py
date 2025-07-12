"""Core exception types"""


class AysekaiError(Exception):
    """Base exception for all Aysekai errors"""

    pass


class ValidationError(AysekaiError):
    """Input validation errors"""

    pass


class DataError(AysekaiError):
    """Data-related errors"""

    pass


class ConfigurationError(AysekaiError):
    """Configuration errors"""

    pass

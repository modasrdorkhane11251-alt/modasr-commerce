"""Structured logging configuration."""
import logging
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger
from app.core.config import settings


class RequestIDFilter(logging.Filter):
    """Add request ID to log records."""
    
    def filter(self, record):
        # Request ID will be set by middleware
        if not hasattr(record, 'request_id'):
            record.request_id = 'unknown'
        return True


def setup_logging():
    """Configure structured logging."""
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    
    # Remove default handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler with JSON formatter
    console_handler = logging.StreamHandler()
    
    if settings.DEBUG:
        # Human-readable format for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        # JSON format for production
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s %(request_id)s',
            timestamp=True
        )
    
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIDFilter())
    root_logger.addHandler(console_handler)
    
    # Reduce noise from noisy libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    return root_logger

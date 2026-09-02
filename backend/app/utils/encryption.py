"""Encryption utilities for sensitive data."""
from cryptography.fernet import Fernet
from app.core.config import settings
import base64

# Initialize cipher
cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_data(data: str) -> str:
    """
    Encrypt sensitive data.
    
    Args:
        data: Plain text data
    
    Returns:
        Encrypted data
    """
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """
    Decrypt sensitive data.
    
    Args:
        encrypted_data: Encrypted data
    
    Returns:
        Plain text data
    """
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

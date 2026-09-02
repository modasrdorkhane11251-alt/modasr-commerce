"""Password hashing and verification."""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

pwd_context = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash password using Argon2id.
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
    
    Returns:
        True if password matches, False otherwise
    """
    try:
        pwd_context.verify(hashed_password, plain_password)
        return True
    except (VerifyMismatchError, VerificationError):
        return False

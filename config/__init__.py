"""
Configuration package for the Healthcare Management System.
"""

from .sql_config import SQL
from .email_config import Email

__all__ = [
    'SQL',
    'Email'
]

"""
SQL Database Configuration
Contains database connection settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get required environment variables
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Validate that required environment variables are set
if not DB_PASSWORD:
    raise ValueError(
        "Missing required environment variable: DB_PASSWORD\n"
        "Please add it to your .env file:\n"
        "DB_PASSWORD=your_database_password"
    )


class SQL:
    """SQL Database Configuration"""

    host = "localhost"
    user = "root"
    password = DB_PASSWORD
    database = "healthcare_management"

# Made with Bob

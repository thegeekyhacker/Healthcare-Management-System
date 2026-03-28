"""
Email Configuration
Contains email settings for sending bills to patients.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get required environment variables
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Validate that required environment variables are set
missing_vars = []
if not EMAIL_SENDER:
    missing_vars.append("EMAIL_SENDER")
if not EMAIL_PASSWORD:
    missing_vars.append("EMAIL_PASSWORD")

if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}\n"
        f"Please add them to your .env file:\n"
        f"EMAIL_SENDER=your_email@gmail.com\n"
        f"EMAIL_PASSWORD=your_app_password"
    )


class Email:
    """Email Configuration"""

    sender = EMAIL_SENDER
    password = EMAIL_PASSWORD
    subject = "Your Bill"
    body = "Kindly find your bill attached.\nThank you for choosing our hospital."
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

# Made with Bob

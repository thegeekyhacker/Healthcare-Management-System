"""
Email Configuration
Contains email settings for sending bills to patients.
"""


class Email:
    """Email Configuration"""

    sender = "utkarshtiwary2004@gmail.com"
    password = "ijoc tysj nffb ****"  # Replace with your app password
    subject = "Your Bill"
    body = "Kindly find your bill attached.\nThank you for choosing our hospital."
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
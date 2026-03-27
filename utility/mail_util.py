"""
Email Utility Module
Provides functions for sending bills via email.
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from config import Email


def send_bill_email(receiver_email, bill_filename, bill_type="opd"):
    """
    Send a bill via email to a patient.

    Args:
        receiver_email (str): Recipient's email address
        bill_filename (str): Name of the bill file (without .pdf extension)
        bill_type (str): Type of bill - 'opd' or 'hospital' (default: 'opd')

    Example:
        send_bill_email('patient@example.com', 'O1_bill', 'opd')
        send_bill_email('patient@example.com', 'B1_bill', 'hospital')
    """
    # Determine the correct folder based on bill type
    if bill_type.lower() == "hospital":
        pdf_folder = "bills/hbill"
    else:
        pdf_folder = "bills/opdbill"

    # Create a multipart message container
    msg = MIMEMultipart()
    msg["From"] = Email.sender
    msg["To"] = receiver_email
    msg["Subject"] = Email.subject

    # Attach body as plain text
    msg.attach(MIMEText(Email.body, "plain"))

    # Attach PDF file
    pdf_attachment_path = f"{pdf_folder}/{bill_filename}.pdf"
    with open(pdf_attachment_path, "rb") as file:
        pdf_attachment = MIMEApplication(file.read(), _subtype="pdf")
        pdf_attachment.add_header(
            "Content-Disposition", "attachment", filename="bill.pdf"
        )
        msg.attach(pdf_attachment)

    # Create an SMTP connection with STARTTLS
    with smtplib.SMTP(Email.smtp_server, Email.smtp_port) as smtp:
        # Start TLS encryption
        smtp.starttls()

        # Log in to the email account
        smtp.login(Email.sender, Email.password)

        # Send the email
        smtp.sendmail(Email.sender, receiver_email, msg.as_string())


# Backward compatibility aliases
def email(receivermail, fname):
    """Legacy function for OPD bills - for backward compatibility"""
    send_bill_email(receivermail, fname, "opd")

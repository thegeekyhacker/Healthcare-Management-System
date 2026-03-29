"""
Email Utility Module
Provides functions for sending bills and generic emails.
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import os
from config import Email


def send_generic_email(receiver_email, subject, body, attachment_path=None):
    """
    Send a generic email with optional attachment.

    Args:
        receiver_email (str): Recipient's email address
        subject (str): Email subject line
        body (str): Email body text
        attachment_path (str, optional): Path to file to attach (default: None)

    Returns:
        dict: Status dictionary with 'success' (bool) and 'message' (str)

    Example:
        send_generic_email('patient@example.com', 'Appointment Reminder', 'Your appointment is tomorrow.')
        send_generic_email('patient@example.com', 'Report', 'See attached', 'reports/report.pdf')
    """
    try:
        # Create a multipart message container
        msg = MIMEMultipart()
        msg["From"] = Email.sender
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Attach body as plain text
        msg.attach(MIMEText(body, "plain"))

        # Attach file if provided
        if attachment_path and os.path.exists(attachment_path):
            filename = os.path.basename(attachment_path)
            with open(attachment_path, "rb") as file:
                # Determine attachment type based on extension
                ext = os.path.splitext(filename)[1].lower()
                if ext == '.pdf':
                    attachment = MIMEApplication(file.read(), _subtype="pdf")
                else:
                    attachment = MIMEApplication(file.read())
                
                attachment.add_header(
                    "Content-Disposition", "attachment", filename=filename
                )
                msg.attach(attachment)

        # Create an SMTP connection with STARTTLS
        with smtplib.SMTP(Email.smtp_server, Email.smtp_port) as smtp:
            # Start TLS encryption
            smtp.starttls()

            # Log in to the email account
            smtp.login(Email.sender, Email.password)

            # Send the email
            smtp.sendmail(Email.sender, receiver_email, msg.as_string())

        return {"success": True, "message": f"Email sent successfully to {receiver_email}"}

    except FileNotFoundError:
        return {"success": False, "message": f"Attachment file not found: {attachment_path}"}
    except smtplib.SMTPAuthenticationError:
        return {"success": False, "message": "SMTP authentication failed. Check email credentials."}
    except smtplib.SMTPException as e:
        return {"success": False, "message": f"SMTP error: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": f"Error sending email: {str(e)}"}


def send_bill_email(receiver_email, bill_filename, bill_type="opd"):
    """
    Send a bill via email to a patient.

    Args:
        receiver_email (str): Recipient's email address
        bill_filename (str): Name of the bill file (without .pdf extension)
        bill_type (str): Type of bill - 'opd' or 'hospital' (default: 'opd')

    Returns:
        dict: Status dictionary with 'success' (bool) and 'message' (str)

    Example:
        send_bill_email('patient@example.com', 'O1_bill', 'opd')
        send_bill_email('patient@example.com', 'B1_bill', 'hospital')
    """
    try:
        # Determine the correct folder based on bill type
        if bill_type.lower() == "hospital":
            pdf_folder = "bills/hbill"
            subject = "Your Hospital Bill"
        else:
            pdf_folder = "bills/opdbill"
            subject = "Your OPD Bill"

        # Build the PDF path
        pdf_attachment_path = f"{pdf_folder}/{bill_filename}.pdf"

        # Check if file exists
        if not os.path.exists(pdf_attachment_path):
            return {"success": False, "message": f"Bill file not found: {pdf_attachment_path}"}

        # Use generic email function with bill-specific defaults
        body = "Kindly find your bill attached.\nThank you for choosing our hospital."
        return send_generic_email(receiver_email, subject, body, pdf_attachment_path)

    except Exception as e:
        return {"success": False, "message": f"Error sending bill email: {str(e)}"}


# Backward compatibility aliases
def email(receivermail, fname):
    """Legacy function for OPD bills - for backward compatibility"""
    send_bill_email(receivermail, fname, "opd")

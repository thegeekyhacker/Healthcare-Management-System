from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib

email_sender = 'utkarsh.tiwary2021@vitstudent.ac.in'
email_password = '**** **** **** ****'
subject = 'Your Bill'
body = f"Kindly find your bill attached.\nThank you for choosing our hospital."

def email(receivermail,fname):
    email_receiver = receivermail

    # Create a multipart message container
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject

    # Attach body as plain text
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF file
    pdf_attachment_path = f'bills/hbill/{fname}.pdf'
    with open(pdf_attachment_path, 'rb') as file:
        pdf_attachment = MIMEApplication(file.read(), _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename='file.pdf')
        msg.attach(pdf_attachment)

    # Create an SMTP connection with STARTTLS
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        # Start TLS encryption
        smtp.starttls()

        # Log in to your Gmail account
        smtp.login(email_sender, email_password)

        # Send the email
        smtp.sendmail(email_sender, email_receiver, msg.as_string())


# email('jayesh.kankaria2021@vitstudent.ac.in','O1_bill')

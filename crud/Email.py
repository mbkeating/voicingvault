from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os

async def send_email(message: str):
    # Connect to the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        print(message)
        server.login(os.getenv("EMAIL_ADDR"), os.getenv("EMAIL_PASS"))

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL_ADDR")
        msg['To'] = os.getenv("EMAIL_ADDR")
        msg['Subject'] = 'New Beta Tester Application'
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server.sendmail(os.getenv("EMAIL_ADDR"), os.getenv("EMAIL_ADDR"), msg.as_string())

    return True
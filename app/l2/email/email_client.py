# email/client.py

# lib
import aiosmtplib
from typing import Any
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# definition

class EmailClient:
    def __init__(self, smtp_server:str, smtp_port:int, email_address:str, email_password:str) -> None:
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.email_password = email_password

    async def send_email(self, to:str, subject:str, subtype:str, body:Any):
        try:
            email = MIMEMultipart()
            email["From"] = self.email_address
            email["To"] = to
            email["Subject"] = subject
            email.attach(
                MIMEText(
                    _text = body,
                    _subtype = subtype
                )
            )
            await aiosmtplib.send(
                email,
                hostname= self.smtp_server,
                port= self.smtp_port,
                start_tls=True,
                username=self.email_address,
                password=self.email_password,

            )
            print(f"sent email to {to}")
            return True
        
        except Exception as e:
            print("Error form send_mail : ", e)
            return False

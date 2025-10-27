import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Send_Email_Utility(object):
    sender: str
    key: str
    server: smtplib.SMTP_SSL

    @staticmethod
    def send_mail(recipients: str, subject: list, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = Send_Email_Utility.sender
        msg["To"] = ", ".join(recipients)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(Send_Email_Utility.sender, Send_Email_Utility.key)
                server.sendmail(Send_Email_Utility.sender, recipients, msg.as_string())
            print("Send mail successful")
        except Exception as e:
            print(f"Error: {str(e)}")


def load_settings_smtp_email(sender: str, key: str):
    # print(f"Username: {sender}")
    # print(f"Password: {key}")
    Send_Email_Utility.sender = sender
    Send_Email_Utility.key = key
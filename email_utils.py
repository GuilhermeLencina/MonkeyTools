# email_utils.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_reset_email(to_email, reset_link):
    smtp_server = os.getenv('MAIL_SERVER')
    smtp_port = int(os.getenv('MAIL_PORT'))
    smtp_username = os.getenv('MAIL_USERNAME')
    smtp_password = os.getenv('MAIL_PASSWORD')
    from_email = smtp_username

    subject = "Recuperação de Senha - MonkeyTools"
    body = f"""
Olá!

Recebemos uma solicitação para redefinir sua senha.

Clique no link abaixo para escolher uma nova senha:
{reset_link}

Se você não solicitou isso, apenas ignore este email.

Abraços,
Equipe MonkeyTools
"""

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"E-mail de recuperação enviado para {to_email}.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

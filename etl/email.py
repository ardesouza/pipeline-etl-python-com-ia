import logging
import os
import smtplib
import ssl

logger = logging.getLogger(__name__)

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(to_email, subject, body):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        raise ValueError(
            "Credenciais do Gmail não encontradas no arquivo .env"
        )

    message = EmailMessage()
    message["From"] = EMAIL_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(message)

    logger.info("E-mail enviado com sucesso para %s.", to_email)



def send_messages_by_email(messages):
    sent = 0
    skipped = 0
    failed = 0

    for item in messages:
        email = item.get("email")
        name = item.get("name", "Cliente")
        message = item.get("message")

        if not email:
            logger.info(
                "E-mail não cadastrado para %s. Envio ignorado.",
                name
            )
            skipped += 1
            continue

        subject = "Uma mensagem de educação financeira para você"

        body = f"""Olá, {name}!

{message}

Atenciosamente,
Equipe de Atendimento
"""

        try:
            send_email(email, subject, body)

            logger.info(
                "E-mail enviado com sucesso para %s.",
                name
            )
            sent += 1

        except Exception:
            logger.exception(
                "Falha ao enviar e-mail para %s.",
                name
            )
            failed += 1
    return {
        "sent": sent,
        "skipped": skipped,
        "failed": failed
    }

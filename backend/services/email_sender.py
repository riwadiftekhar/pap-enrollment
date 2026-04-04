import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from backend.config import settings


def send_pdf(recipient: str, pdf_bytes: bytes, patient_name: str) -> None:
    msg = MIMEMultipart("mixed")
    msg["From"] = settings.smtp_user
    msg["To"] = recipient
    msg["Subject"] = f"Sanofi PAP Enrollment – {patient_name}"

    body = MIMEText(
        f"Please find attached the completed Sanofi Patient Connection enrollment form for {patient_name}.\n\n"
        "Review the document, obtain required signatures, and submit to:\n"
        "Sanofi Patient Connection\n"
        "P.O. Box 222138 · Charlotte, NC · 28222-2138\n"
        "Phone: 1-888-847-4877 | Fax: 1-888-847-1797",
        "plain",
    )
    msg.attach(body)

    attachment = MIMEApplication(pdf_bytes, Name="Sanofi_PAP_Enrollment.pdf")
    attachment["Content-Disposition"] = 'attachment; filename="Sanofi_PAP_Enrollment.pdf"'
    msg.attach(attachment)

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.smtp_host, 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.smtp_user, recipient, msg.as_bytes())

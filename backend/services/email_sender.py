import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from backend.config import settings


def send_pdf(
    recipient: str,
    pdf_bytes: bytes,
    patient_name: str,
    program_display_name: str = "PAP",
    pdf_filename: str = "PAP_Enrollment.pdf",
    email_body: str = None,
) -> None:
    msg = MIMEMultipart("mixed")
    msg["From"] = settings.smtp_user
    msg["To"] = recipient
    msg["Subject"] = f"{program_display_name} Enrollment \u2013 {patient_name}"

    if email_body is None:
        email_body = (
            f"Please find attached the completed {program_display_name} enrollment form "
            f"for {patient_name}.\n\n"
            "Review the document, obtain the required patient and prescriber signatures, "
            "then submit it to the program per the instructions on the form."
        )

    msg.attach(MIMEText(email_body, "plain"))

    attachment = MIMEApplication(pdf_bytes, Name=pdf_filename)
    attachment["Content-Disposition"] = f'attachment; filename="{pdf_filename}"'
    msg.attach(attachment)

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.smtp_host, 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.smtp_user, recipient, msg.as_bytes())

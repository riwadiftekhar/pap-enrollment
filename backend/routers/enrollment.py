from fastapi import APIRouter, HTTPException
from backend.models.enrollment import EnrollmentData
from backend.services.pdf_filler import fill_sanofi_pdf
from backend.services.email_sender import send_pdf

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/enroll")
def enroll(data: EnrollmentData):
    try:
        pdf_bytes = fill_sanofi_pdf(data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    patient_name = f"{data.patient_first_name} {data.patient_last_name}"

    try:
        send_pdf(
            recipient=data.recipient_email,
            pdf_bytes=pdf_bytes,
            patient_name=patient_name,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

    return {
        "status": "success",
        "message": f"Enrollment PDF sent to {data.patient_email}",
    }

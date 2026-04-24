from fastapi import APIRouter, HTTPException
from backend.models.enrollment import EnrollmentData
from backend.programs import PROGRAMS
from backend.services.email_sender import send_pdf

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/programs")
def list_programs():
    """Return the list of available enrollment programs for the frontend selector."""
    return [
        {"id": program_id, "name": module.DISPLAY_NAME, "subtitle": module.SUBTITLE}
        for program_id, module in PROGRAMS.items()
    ]


@router.post("/enroll/{program}")
def enroll(program: str, data: EnrollmentData):
    if program not in PROGRAMS:
        raise HTTPException(status_code=404, detail=f"Unknown program: {program}")

    try:
        pdf_bytes = PROGRAMS[program].fill_pdf(data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    patient_name = f"{data.patient_first_name} {data.patient_last_name}"
    program_module = PROGRAMS[program]

    try:
        send_pdf(
            recipient=data.recipient_email,
            pdf_bytes=pdf_bytes,
            patient_name=patient_name,
            program_display_name=program_module.DISPLAY_NAME,
            pdf_filename=getattr(program_module, "PDF_FILENAME", f"{program}_enrollment.pdf"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

    return {
        "status": "success",
        "message": f"Enrollment PDF sent to {data.recipient_email}",
    }

"""
Sanofi Patient Connection® — PAP enrollment program.

Exports required by the program registry:
  DISPLAY_NAME  str   — shown on the program selector card
  SUBTITLE      str   — shown below the display name
  fill_pdf      func  — fill_pdf(data: dict) -> bytes
"""
from pathlib import Path
from backend.services.pdf_utils import fill_pdf_form

DISPLAY_NAME = "Sanofi"
SUBTITLE = "Patient Connection®"

_TEMPLATE = Path(__file__).parent.parent / "assets" / "sanofi_pap_template.pdf"


def fill_pdf(data: dict) -> bytes:
    return fill_pdf_form(_TEMPLATE, _build_field_map(data), _build_radio_map(data))


def _build_field_map(data: dict) -> dict:
    """Map form keys to exact Sanofi PDF text field names."""
    patient_full_name = (
        f"{data.get('patient_first_name', '')} {data.get('patient_last_name', '')}".strip()
    )

    fields = {
        # Patient Info (Section 1)
        "Patient first name": data.get("patient_first_name", ""),
        "Patient middle initial": data.get("patient_middle_initial", ""),
        "Patint last name": data.get("patient_last_name", ""),  # typo in PDF preserved
        "Patient SSN": data.get("patient_ssn", ""),
        "Patient DOB MM": data.get("patient_dob_mm", ""),
        "Patient DOB DD": data.get("patient_dob_dd", ""),
        "Patient DOB YYYY": data.get("patient_dob_yyyy", ""),
        "Patient Address": data.get("patient_address", ""),
        "Patient City": data.get("patient_city", ""),
        "Patient State": data.get("patient_state", ""),
        "Patient Zip": data.get("patient_zip", ""),
        "Patient preferred language": data.get("patient_preferred_language", ""),
        "Patient phone 1st 3": data.get("patient_phone_1", ""),
        "Patient phone 2nd 3": data.get("patient_phone_2", ""),
        "Patient phone last 4": data.get("patient_phone_3", ""),
        "Patient email": data.get("patient_email", ""),
        "Annual household income": data.get("annual_household_income", ""),
        "Household other #": data.get("household_other_number", ""),

        # Section 4 repeats patient name and DOB
        "Patient name": patient_full_name,
        "Patient DOB MM 2": data.get("patient_dob_mm", ""),
        "Patient DOB DD 2": data.get("patient_dob_dd", ""),
        "Patient DOB YYYY 2": data.get("patient_dob_yyyy", ""),

        # Medication 1
        "Medication #1": data.get("medication_1_name", ""),
        "Medication #1 ICD-10 Code": data.get("medication_1_icd10", ""),
        "Medication #1 Frequency": data.get("medication_1_frequency", ""),
        "Medication #1 Dosage": data.get("medication_1_dosage", ""),
        "Medication #1 Qty": data.get("medication_1_qty", ""),

        # Medication 2
        "Medication #2": data.get("medication_2_name", ""),
        "Medication #2 ICD-10 Code": data.get("medication_2_icd10", ""),
        "Medication #2 Frequency": data.get("medication_2_frequency", ""),
        "Medication #2 Dosage": data.get("medication_2_dosage", ""),
        "Medication #2 Qty": data.get("medication_2_qty", ""),

        # Prescriber
        "Prescriber name": data.get("prescriber_name", ""),
        "State where licensed": data.get("prescriber_state", ""),
        "License #": data.get("prescriber_license", ""),
        "NPI #": data.get("prescriber_npi", ""),
    }

    return {k: v for k, v in fields.items() if v}


def _build_radio_map(data: dict) -> dict:
    """Map radio button groups to their PDF export values."""
    radio = {}

    # Household size: /1 /2 /3 /4 /5 /Other
    hi = data.get("household_income", "")
    if hi:
        radio["Household income"] = f"/{hi}"

    # Medication formulation: /Vials /Pens /N/a
    m1 = data.get("medication_1_type", "")
    if m1:
        radio["Medication 1"] = f"/{m1}"

    m2 = data.get("medication_2_type", "")
    if m2:
        radio["Medication 2"] = f"/{m2}"

    return radio

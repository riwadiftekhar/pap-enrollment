from pydantic import BaseModel, EmailStr
from typing import Optional


class EnrollmentData(BaseModel):
    # Patient Information
    patient_first_name: str
    patient_middle_initial: Optional[str] = ""
    patient_last_name: str
    patient_ssn: Optional[str] = ""
    patient_dob_mm: str
    patient_dob_dd: str
    patient_dob_yyyy: str
    patient_address: str
    patient_city: str
    patient_state: str
    patient_zip: str
    patient_preferred_language: Optional[str] = ""
    patient_phone_1: str  # first 3 digits
    patient_phone_2: str  # middle 3 digits
    patient_phone_3: str  # last 4 digits
    patient_email: str
    recipient_email: str
    household_income: Optional[str] = ""   # "1","2","3","4","5","6","7plus"
    annual_household_income: Optional[str] = ""

    # Medication 1
    medication_1_name: Optional[str] = ""
    medication_1_icd10: Optional[str] = ""
    medication_1_frequency: Optional[str] = ""
    medication_1_dosage: Optional[str] = ""
    medication_1_qty: Optional[str] = ""
    medication_1_type: Optional[str] = ""   # "Vials", "Pens", or "N/a"

    # Medication 2
    medication_2_name: Optional[str] = ""
    medication_2_icd10: Optional[str] = ""
    medication_2_frequency: Optional[str] = ""
    medication_2_dosage: Optional[str] = ""
    medication_2_qty: Optional[str] = ""
    medication_2_type: Optional[str] = ""   # "Vials", "Pens", or "N/a"

    # Prescriber
    prescriber_name: str
    prescriber_state: Optional[str] = ""
    prescriber_license: Optional[str] = ""
    prescriber_npi: Optional[str] = ""

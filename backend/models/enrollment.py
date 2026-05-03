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

    # LillyCares-specific fields
    lc_household_size: Optional[str] = ""
    lc_annual_household_income: Optional[str] = ""
    medication_requested: Optional[str] = ""
    lc_allergies: Optional[str] = ""
    lc_other_medications: Optional[str] = ""
    lc_medication: Optional[str] = ""
    lc_strength: Optional[str] = ""
    lc_max_dose_per_day: Optional[str] = ""
    lc_directions: Optional[str] = ""
    lc_prescribing_insulin: Optional[str] = ""
    lc_insulin_type: Optional[str] = ""
    lc_refills: Optional[str] = ""
    lc_hcp_name_title: Optional[str] = ""
    lc_state_license: Optional[str] = ""
    lc_npi: Optional[str] = ""

    # BI Cares-specific fields
    bi_sex: Optional[str] = ""
    bi_household_size: Optional[str] = ""
    bi_allergies: Optional[str] = ""
    bi_current_medications: Optional[str] = ""
    bi_health_conditions: Optional[str] = ""
    bi_medication: Optional[str] = ""
    bi_strength: Optional[str] = ""
    bi_directions: Optional[str] = ""
    bi_refills: Optional[str] = ""

"""
LillyCares Foundation® — PAP enrollment program.

Exports required by the program registry:
  DISPLAY_NAME  str   — shown on the program selector card
  SUBTITLE      str   — shown below the display name
  fill_pdf      func  — fill_pdf(data: dict) -> bytes

PDF field names are generic (e.g. "Text Field 158") — mapped from
coordinate analysis. Fields filled across pages 4, 8, and 9 only.
"""
import datetime
from pathlib import Path
from backend.services.pdf_utils import fill_pdf_form_pdfrw

DISPLAY_NAME = "LillyCares"
SUBTITLE = "Lilly Cares Foundation®"
PDF_FILENAME = "LillyCares_PAP_Enrollment.pdf"

OFFICE_CONTACT_NAME = "Katie McClendon"
OFFICE_PHONE = "601-355-5161"
OFFICE_FAX = "601-398-0601"
OFFICE_ADDRESS = "2466 Flowood Dr"
OFFICE_CITY = "Flowood"
OFFICE_STATE = "MS"
OFFICE_ZIP = "39232"

_TEMPLATE = Path(__file__).parent.parent / "assets" / "lillycares_pap_template.pdf"


def fill_pdf(data: dict) -> bytes:
    return fill_pdf_form_pdfrw(_TEMPLATE, _build_field_map(data), _build_radio_map(data))


def _build_field_map(data: dict) -> dict:
    """Map form keys to LillyCares PDF text field names (pages 4, 8, 9)."""
    patient_full_name = (
        f"{data.get('patient_first_name', '')} {data.get('patient_last_name', '')}".strip()
    )
    patient_dob = (
        f"{data.get('patient_dob_mm', '')}/"
        f"{data.get('patient_dob_dd', '')}/"
        f"{data.get('patient_dob_yyyy', '')}"
    )
    patient_phone = (
        f"{data.get('patient_phone_1', '')}-"
        f"{data.get('patient_phone_2', '')}-"
        f"{data.get('patient_phone_3', '')}"
    )
    date_today = datetime.date.today().strftime("%m/%d/%Y")

    fields = {
        # --- Page 4: Patient Information ---
        "Text Field 158": data.get("patient_first_name", ""),
        "Text Field 167": data.get("patient_middle_initial", ""),
        "Text Field 165": data.get("patient_last_name", ""),
        "Text Field 164": data.get("patient_address", ""),
        "Text Field 159": data.get("patient_city", ""),
        "Text Field 168": data.get("patient_state", ""),
        "Text Field 166": data.get("patient_zip", ""),
        "Text Field 163": patient_dob,
        "Text Field 169": patient_phone,
        "Text Field 160": data.get("lc_household_size", ""),
        "Text Field 170": data.get("lc_annual_household_income", "") or data.get("annual_household_income", ""),

        # --- Page 8: Prescription Request (top section only) ---
        "Text Field 181": patient_full_name,
        "Text Field 237": patient_dob,
        "Text Field 182": data.get("medication_requested", ""),
        "Text Field 236": OFFICE_CONTACT_NAME,
        "Text Field 234": OFFICE_PHONE,
        "Text Field 233": OFFICE_FAX,
        "Text Field 232": date_today,
        "Text Field 227": data.get("lc_hcp_name_title", ""),

        # --- Page 9: Clinical & Prescriber ---
        "Text Field 194": patient_full_name,
        "Text Field 217": patient_dob,
        "Text Field 195": data.get("patient_address", ""),
        "Text Field 197": patient_phone,
        "Text Field 207": data.get("patient_city", ""),
        "Text Field 210": data.get("patient_state", ""),
        "Text Field 220": data.get("patient_zip", ""),
        "Text Field 196": data.get("lc_allergies", ""),
        "Text Field 208": data.get("lc_other_medications", ""),
        "Text Field 211": data.get("lc_medication", ""),
        "Text Field 212": data.get("lc_strength", ""),
        "Text Field 199": data.get("lc_max_dose_per_day", ""),
        "Text Field 221": data.get("lc_directions", ""),
        "Text Field 218": date_today,
        "Text Field 200": data.get("lc_hcp_name_title", ""),
        "Text Field 201": data.get("lc_state_license", ""),
        "Text Field 204": data.get("lc_npi", ""),
        "Text Field 203": OFFICE_ADDRESS,
        "Text Field 209": OFFICE_CITY,
        "Text Field 213": OFFICE_STATE,
        "Text Field 214": OFFICE_ZIP,
        "Text Field 215": OFFICE_PHONE,
        "Text Field 216": OFFICE_FAX,
        "Text Field 202": OFFICE_CONTACT_NAME,
        "Text Field 205": OFFICE_PHONE,
    }

    return {k: v for k, v in fields.items() if v}


def _build_radio_map(data: dict) -> dict:
    """Map radio button groups to their PDF export values (page 9)."""
    radio = {}

    # Are you prescribing insulin? Choice1=Yes, Choice2=No
    insulin = data.get("lc_prescribing_insulin", "")
    if insulin == "Yes":
        radio["Radio Button 8"] = "/Choice1"
    elif insulin == "No":
        radio["Radio Button 8"] = "/Choice2"

    # Insulin type: Choice1=KwikPen, Choice2=Vial, Choice3=Cartridge
    insulin_type = data.get("lc_insulin_type", "")
    type_map = {"KwikPen": "/Choice1", "Vial": "/Choice2", "Cartridge": "/Choice3"}
    if insulin_type in type_map:
        radio["Radio Button 11"] = type_map[insulin_type]

    # Refills: Choice1=0, Choice2=1, Choice3=2, Choice4=3
    refills = data.get("lc_refills", "")
    refill_map = {"0": "/Choice1", "1": "/Choice2", "2": "/Choice3", "3": "/Choice4"}
    if refills in refill_map:
        radio["Radio Button 9"] = refill_map[refills]

    return radio

"""
Boehringer Ingelheim Cares Foundation® — PAP enrollment program.

Exports required by the program registry:
  DISPLAY_NAME  str   — shown on the program selector card
  SUBTITLE      str   — shown below the display name
  fill_pdf      func  — fill_pdf(data: dict) -> bytes
"""
from pathlib import Path
from backend.services.pdf_utils import fill_pdf_form_pdfrw

DISPLAY_NAME = "BI Cares"
SUBTITLE = "Boehringer Ingelheim Cares Foundation®"
PDF_FILENAME = "BI_Cares_PAP_Enrollment.pdf"

# Pre-filled office constants
OFFICE_SITE    = "Flowood Family Medicine"
OFFICE_CONTACT = "Katie McClendon"
OFFICE_ADDRESS = "2466 Flowood Dr"
OFFICE_CITY    = "Flowood"
OFFICE_STATE   = "MS"
OFFICE_ZIP     = "39232"
OFFICE_PHONE   = "601-355-5161"
OFFICE_FAX     = "601-398-0601"
OFFICE_EMAIL   = "arnob@jfchealth.org"

_TEMPLATE = Path(__file__).parent.parent / "assets" / "bicares_pap_template.pdf"

# ---------------------------------------------------------------------------
# Medication map — keyed by the display name shown in the frontend dropdown.
# Each entry describes how to fill page 2, page 5, and refills for that med.
#   page2_cb       : checkbox field name on page 2 (Section 1)
#   page5_cb       : checkbox field name on page 5 (Section 8)
#   directions_field: text field name for directions on page 5
#   strength_field : text field name for strength on page 5 (None = pre-filled)
#   refill_group   : radio group name for the refill selection on page 5
#   refill_values  : {count_str: pdf_export_value}
# ---------------------------------------------------------------------------
MEDICATION_MAP = {
    "Aptivus® Capsules": {
        "page2_cb": "Check Box129",
        "page5_cb": "Check Box164",
        "directions_field": "Directions250mg",
        "strength_field": None,
        "refill_group": "Group191",
        "refill_values": {"1": "/Choice3", "2": "/Choice4", "3": "/Choice6"},
    },
    "Atrovent® HFA": {
        "page2_cb": "Check Box130",
        "page5_cb": "Check Box165",
        "directions_field": "Directions17mcgact",
        "strength_field": None,
        "refill_group": "Group192",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
    "Combivent® Respimat®": {
        "page2_cb": "Check Box132",
        "page5_cb": "Check Box166",
        "directions_field": "Directions20mc100cg per act",
        "strength_field": None,
        "refill_group": "Group193",
        "refill_values": {"1": "/Choice3", "2": "/Choice4", "3": "/Choice6"},
    },
    "Cyltezo®": {
        "page2_cb": "Check Box136",
        "page5_cb": "Check Box167",
        "directions_field": "DirectionsCyltezo",
        "strength_field": "20mc100cg per actCyltezo",
        "refill_group": "Group194",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
    "Gilotrif®": {
        "page2_cb": "Check Box137",
        "page5_cb": "Check Box168",
        "directions_field": "DirectionsGilotrif",
        "strength_field": "20mc100cg per actGilotrif",
        "refill_group": "Group195",
        "refill_values": {"1": "/Choice3", "2": "/Choice4", "3": "/Choice6"},
    },
    "Glyxambi®": {
        "page2_cb": "Check Box140",
        "page5_cb": "Check Box169",
        "directions_field": "DirectionsGlyxambi",
        "strength_field": "20mc100cg per actGlyxambi",
        "refill_group": "Group196",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
    "Jardiance®": {
        "page2_cb": "Check Box141",
        "page5_cb": "Check Box170",
        "directions_field": "DirectionsJardiance",
        "strength_field": "20mc100cg per actJardiance",
        "refill_group": "Group197",
        "refill_values": {"1": "/Choice3", "2": "/Choice4", "3": "/Choice6"},
    },
    "Jentadueto®": {
        "page2_cb": "Check Box142",
        "page5_cb": "Check Box171",
        "directions_field": "DirectionsJentadueto",
        "strength_field": "20mc100cg per actJentadueto",
        "refill_group": "198",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
    "Jentadueto® XR": {
        "page2_cb": "Check Box143",
        "page5_cb": "Check Box172",
        "directions_field": "DirectionsJentadueto XR",
        "strength_field": "20mc100cg per actJentadueto XR",
        "refill_group": "199",
        "refill_values": {"1": "/2", "2": "/0", "3": "/1"},
    },
    "Ofev®": {
        "page2_cb": "Check Box144",
        "page5_cb": "Check Box173",
        "directions_field": "DirectionsOfev",
        "strength_field": "20mc100cg per actOfev",
        "refill_group": "200",
        "refill_values": {"1": "/2", "2": "/1", "3": "/0"},
    },
    "Spiriva® Respimat® 2.5mcg": {
        "page2_cb": "Check Box146",
        "page5_cb": "Check Box177",
        "directions_field": "Directions25mcgact",
        "strength_field": None,
        "refill_group": "203",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
    "Spiriva® Respimat® 1.25mcg": {
        "page2_cb": "Check Box146",
        "page5_cb": "Check Box178",
        "directions_field": "Directions125mcgact",
        "strength_field": None,
        "refill_group": "204",
        "refill_values": {"1": "/Choice3", "2": "/Choice4", "3": "/Choice6"},
    },
    "Stiolto® Respimat®": {
        "page2_cb": "Check Box147",
        "page5_cb": "Check Box179",
        "directions_field": "Directions25mcg25mcg per act",
        "strength_field": None,
        "refill_group": "205",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
    "Striverdi® Respimat®": {
        "page2_cb": "Check Box148",
        "page5_cb": "Check Box180",
        "directions_field": "Directions25mcgact_2",
        "strength_field": None,
        "refill_group": "206",
        "refill_values": {"1": "/Choice3", "2": "/Choice4", "3": "/Choice6"},
    },
    "Synjardy®": {
        "page2_cb": "Check Box149",
        "page5_cb": "Check Box181",
        "directions_field": "DirectionsSynjardy",
        "strength_field": "25mcgactSynjardy",
        "refill_group": "207",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
    "Synjardy® XR": {
        "page2_cb": "Check Box150",
        "page5_cb": "Check Box182",
        "directions_field": "DirectionsSynjardy XR",
        "strength_field": "25mcgactSynjardy XR",
        "refill_group": "208",
        "refill_values": {"1": "/Choice3", "2": "/Choice4", "3": "/Choice6"},
    },
    "Tradjenta®": {
        "page2_cb": "Check Box151",
        "page5_cb": "Check Box183",
        "directions_field": "Directions5mg tab",
        "strength_field": None,
        "refill_group": "209",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
    "Trijardy® XR": {
        "page2_cb": "Check Box152",
        "page5_cb": "Check Box184",
        "directions_field": "DirectionsTrijardy XR",
        "strength_field": "5mg tabTrijardy XR",
        "refill_group": "210",
        "refill_values": {"1": "/Choice1", "2": "/Choice2", "3": "/Choice5"},
    },
}


def fill_pdf(data: dict) -> bytes:
    fields      = _build_field_map(data)
    radio       = _build_radio_map(data)
    checkboxes  = _build_checkbox_list(data)
    return fill_pdf_form_pdfrw(_TEMPLATE, fields, radio, checkboxes)


def _build_field_map(data: dict) -> dict:
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

    fields = {
        # --- Page 2: Patient Information ---
        "First Name":           data.get("patient_first_name", ""),
        "Last Name":            data.get("patient_last_name", ""),
        "Address":              data.get("patient_address", ""),
        "City":                 data.get("patient_city", ""),
        "State":                data.get("patient_state", ""),
        "Zip Code":             data.get("patient_zip", ""),
        "DOB MMDDYYYY":         patient_dob,
        "Last 4 Digits of SSN": data.get("patient_ssn", ""),
        "Email Address":        data.get("patient_email", ""),
        "Daytime Phone Number": patient_phone,
        "Number of people in your household including yourself 1":
                                data.get("bi_household_size", ""),
        "Total annual household income per year":
                                data.get("annual_household_income", ""),

        # --- Page 4: Pre-filled office + prescriber ---
        "SiteFacility Name":    OFFICE_SITE,
        "Office Contact Name":  OFFICE_CONTACT,
        "Address-Section6":     OFFICE_ADDRESS,
        "City_2":               OFFICE_CITY,
        "State_2":              OFFICE_STATE,
        "Zip Code_2":           OFFICE_ZIP,
        "Office Phone Number":  OFFICE_PHONE,
        "Office Fax Number":    OFFICE_FAX,
        "Email Address_2":      OFFICE_EMAIL,
        "Prescriber Name":      data.get("prescriber_name", ""),
        "NPI":                  data.get("prescriber_npi", ""),

        # --- Page 5: Patient + clinical ---
        "Patient First Name":   data.get("patient_first_name", ""),
        "Patient Last Name":    data.get("patient_last_name", ""),
        "DOB MMDDYYYY_2":       patient_dob,
        "Allergies":            data.get("bi_allergies", ""),
        "Current Medications":  data.get("bi_current_medications", ""),
        "Health Conditions":    data.get("bi_health_conditions", ""),
        "Prescriber Name_2":    data.get("prescriber_name", ""),
        "NPI_2":                data.get("prescriber_npi", ""),
    }

    # Per-medication directions and strength fields
    med_name = data.get("bi_medication", "")
    if med_name and med_name in MEDICATION_MAP:
        med = MEDICATION_MAP[med_name]
        directions = data.get("bi_directions", "")
        if directions and med["directions_field"]:
            fields[med["directions_field"]] = directions
        strength = data.get("bi_strength", "")
        if strength and med["strength_field"]:
            fields[med["strength_field"]] = strength

    return {k: v for k, v in fields.items() if v}


def _build_radio_map(data: dict) -> dict:
    radio = {}

    # Sex: Group186 — /0 = Male, /1 = Female
    sex = data.get("bi_sex", "")
    if sex == "Male":
        radio["Group186"] = "/0"
    elif sex == "Female":
        radio["Group186"] = "/1"

    # Refills for selected medication
    med_name = data.get("bi_medication", "")
    refills   = data.get("bi_refills", "")
    if med_name and med_name in MEDICATION_MAP and refills:
        med = MEDICATION_MAP[med_name]
        export_val = med["refill_values"].get(refills)
        if export_val:
            radio[med["refill_group"]] = export_val

    return radio


def _build_checkbox_list(data: dict) -> list:
    """Return the list of checkbox field names to mark as checked."""
    checkboxes = []
    med_name = data.get("bi_medication", "")
    if med_name and med_name in MEDICATION_MAP:
        med = MEDICATION_MAP[med_name]
        checkboxes.append(med["page2_cb"])
        checkboxes.append(med["page5_cb"])
    return checkboxes

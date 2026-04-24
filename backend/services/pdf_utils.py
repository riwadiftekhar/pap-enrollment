from pathlib import Path
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
import pdfrw


def fill_pdf_form(template_path: Path, fields: dict, radio_fields: dict = None) -> bytes:
    """Fill an AcroForm PDF template with the given field values and return bytes."""
    reader = PdfReader(str(template_path))
    writer = PdfWriter()
    writer.clone_reader_document_root(reader)

    for page in writer.pages:
        writer.update_page_form_field_values(page, fields)

    if radio_fields:
        _fill_radio_fields(writer, radio_fields)

    writer.set_need_appearances_writer()

    buf = BytesIO()
    writer.write(buf)
    return buf.getvalue()


def _fill_radio_fields(writer: PdfWriter, radio_fields: dict):
    """
    Fill radio button groups by iterating page annotations.

    Radio button kids are widget annotations on pages — they don't have /T
    themselves, but their /Parent does. This is the same object graph that
    update_page_form_field_values uses, so changes here are guaranteed to
    land in the written PDF (avoids the stale-reference issue with
    accessing via writer._root_object[/AcroForm]).
    """
    updated_parents = set()

    for page in writer.pages:
        for annot_ref in page.get("/Annots", []):
            annot = annot_ref.get_object()

            # Skip annotations that have their own /T — those are handled by
            # update_page_form_field_values already
            if annot.get("/T"):
                continue

            parent_ref = annot.get("/Parent")
            if parent_ref is None:
                continue
            parent = parent_ref.get_object()
            field_name = parent.get("/T")

            if field_name not in radio_fields:
                continue

            value = radio_fields[field_name]

            # Update parent /V once per group
            if field_name not in updated_parents:
                parent.update({NameObject("/V"): NameObject(value)})
                updated_parents.add(field_name)

            # Set /AS on this widget: export value if it matches, else /Off
            ap = annot.get("/AP", {})
            n = ap.get("/N", {})
            if hasattr(n, "keys") and NameObject(value) in n:
                annot.update({NameObject("/AS"): NameObject(value)})
            else:
                annot.update({NameObject("/AS"): NameObject("/Off")})


def fill_pdf_form_pdfrw(template_path: Path, fields: dict, radio_fields: dict = None) -> bytes:
    """
    Fill an AcroForm PDF using pdfrw — used for PDFs with generic field names
    (e.g. 'Text Field 158') where pypdf's clone approach fails to persist values.
    """
    template = pdfrw.PdfReader(str(template_path))
    template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))

    # Fill text fields via page annotations
    for page in template.pages:
        if page['/Annots'] is None:
            continue
        for annotation in page['/Annots']:
            if annotation['/Subtype'] != '/Widget':
                continue
            field_name = annotation['/T']
            if field_name is None:
                continue
            clean_name = field_name.strip('()')
            if clean_name in fields and fields[clean_name]:
                annotation.update(pdfrw.PdfDict(V=fields[clean_name]))

    # Fill radio button groups via AcroForm fields tree
    if radio_fields:
        _fill_radio_fields_pdfrw(template, radio_fields)

    buf = BytesIO()
    pdfrw.PdfWriter().write(buf, template)
    return buf.getvalue()


def _fill_radio_fields_pdfrw(template, radio_fields: dict):
    """Set radio button groups using pdfrw field tree traversal."""
    acroform = template.Root.AcroForm
    if acroform is None or acroform.Fields is None:
        return

    def walk(fields_list):
        for field in fields_list:
            name = field['/T']
            if name:
                clean = name.strip('()')
                if clean in radio_fields:
                    value = radio_fields[clean]          # e.g. "/Choice1"
                    pdf_val = pdfrw.PdfName(value.lstrip('/'))
                    field.update(pdfrw.PdfDict(V=pdf_val))
                    # Update each kid widget's /AS
                    kids = field['/Kids']
                    if kids:
                        for kid in kids:
                            ap = kid['/AP']
                            n_dict = ap['/N'] if ap else None
                            if n_dict and hasattr(n_dict, 'keys'):
                                key = pdfrw.PdfName(value.lstrip('/'))
                                if key in n_dict:
                                    kid.update(pdfrw.PdfDict(AS=key))
                                else:
                                    kid.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Off')))
            # Recurse into kids that are field groups (have /T themselves)
            kids = field['/Kids']
            if kids:
                walk(kids)

    walk(acroform.Fields)

"""
Program registry — add new programs here.

To add a new pharmaceutical program:
  1. Create backend/programs/<company>.py  (see sanofi.py as a template)
  2. Import it below and add an entry to PROGRAMS
"""
from backend.programs import sanofi

PROGRAMS: dict = {
    "sanofi": sanofi,
}

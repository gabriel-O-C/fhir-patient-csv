"""Mapping functions for converting between different formats."""

import re
from datetime import datetime

from fhirclient.models.fhirdate import FHIRDate

from .settings import GENDER_MAP


def map_gender(gender: str) -> str:
    """Map gender to FHIR-compatible values. Default to 'unknown'."""
    return GENDER_MAP.get(gender, 'unknown')


def format_phone_number(phone: str) -> str:
    """Remove all non-digit characters from a phone number."""
    return re.sub(r'\D', '', phone)


def format_birth_date(birth_date: str) -> FHIRDate:
    """
    Convert birth date from DD/MM/YYYY to FHIR-compatible YYYY-MM-DD format
    using datetime.
    """
    try:
        parsed_date = datetime.strptime(birth_date, '%d/%m/%Y')
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        return FHIRDate(formatted_date)
    except ValueError:
        return None

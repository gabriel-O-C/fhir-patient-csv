"""Utility functions for handling patient data."""

from typing import List, Tuple

from .mappings import (
    format_birth_date,
    format_phone_number,
    map_gender,
)
from .schema import PatientCsv, key_mapping
from .settings import BRAZILIAN_CPF_SYSTEM


def split_name(name: str) -> Tuple[List[str], str]:
    """Split name into given and family names."""
    parts = name.split()
    given_names = parts[:-1]
    family_name = parts[-1] if parts else ''
    return given_names, family_name


def normalize_patient(patient) -> PatientCsv:
    """Normalize patient data according to key mapping."""
    patient = {key_mapping[key]: value for key, value in patient.items()}
    patient = PatientCsv(**patient)
    return patient


def patient_csv_to_json(patient_csv: PatientCsv) -> dict:
    """Convert PatientCsv to a JSON-like dictionary."""
    given_names, family_name = split_name(patient_csv.name)

    return {
        'name': [
            {'use': 'official', 'given': given_names, 'family': family_name}
        ],
        'identifier': [
            {'system': BRAZILIAN_CPF_SYSTEM, 'value': patient_csv.cpf}
        ],
        'birthDate': str(
            format_birth_date(patient_csv.birth_date).isostring
        ),
        'gender': map_gender(patient_csv.gender),
        'telecom': [
            {
                'system': 'phone',
                'value': format_phone_number(patient_csv.phone),
                'use': 'mobile',
            }
        ],
        'address': [{'country': patient_csv.country}],
    }

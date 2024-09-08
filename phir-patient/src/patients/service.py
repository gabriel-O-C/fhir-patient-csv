import pprint
import re
from datetime import datetime
from typing import List, Tuple

from fhirclient import client
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.condition import Condition
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.observation import Observation
from fhirclient.models.patient import Patient

from src.patients.schema import PatientCsv, key_mapping

BRAZILIAN_CPF_SYSTEM = (
    'urn:oid:2.16.840.1.113883.13.237'  # Example CPF OID for Brazil
)
GENDER_MAP = {'Masculino': 'male', 'Feminino': 'female'}

settings = {'app_id': 'my_web_app', 'api_base': 'http://127.0.0.1:8080/fhir'}

fhir_client = client.FHIRClient(settings)


def map_gender(gender: str) -> str:
    """Map gender to FHIR-compatible values. Default to 'unknown'."""
    mapped_gender = GENDER_MAP.get(gender, 'unknown')
    return mapped_gender


def format_phone_number(phone: str) -> str:
    """Remove all non-digit characters from a phone number."""
    cleaned_phone = re.sub(r'\D', '', phone)
    return cleaned_phone


def format_birth_date(birth_date: str) -> FHIRDate:
    """Convert birth date from DD/MM/YYYY to FHIR-compatible YYYY-MM-DD format using datetime."""
    try:
        parsed_date = datetime.strptime(birth_date, '%d/%m/%Y')
        formatted_date = parsed_date.strftime('%Y-%m-%d')

        return FHIRDate(formatted_date)
    except ValueError:
        return None


def split_name(name: str) -> Tuple[List[str], str]:
    """Split name into given and family names."""
    parts = name.split()
    given_names = parts[:-1]
    family_name = parts[-1] if parts else ''
    return given_names, family_name


def normalize_patient(patient) -> PatientCsv:
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
        'birthDate': str(format_birth_date(patient_csv.birth_date).isostring),
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


def create_diabetes_condition(patient_id: str) -> Condition:
    """Create a FHIR Condition resource for diabetes."""
    condition = Condition()

    condition.code = CodeableConcept({
        'coding': [
            {
                'system': 'http://snomed.info/sct',
                'code': '44054006',
                'display': 'Diabetes mellitus type 2',
            }
        ]
    })

    condition.subject = FHIRReference({'reference': f'Patient/{patient_id}'})

    # condition.onsetDateTime = FHIRDate(datetime.now().strftime('%Y-%m-%d')).isostring

    return condition


def create_hypertension_condition(patient_id: str) -> Condition:
    """Create a FHIR Condition resource for hypertension."""
    condition = Condition()
    print(patient_id, 'patient id')

    condition.code = CodeableConcept({
        'coding': [
            {
                'system': 'http://snomed.info/sct',
                'code': '38341003',
                'display': 'Hypertension',
            }
        ]
    })

    condition.subject = FHIRReference({'reference': f'Patient/{patient_id}'})

    return condition


def create_pregnancy_observation(patient_id: str) -> Observation:
    """Create a FHIR Observation resource for pregnancy."""
    observation = Observation()

    observation.code = CodeableConcept({
        'coding': [
            {
                'system': 'http://snomed.info/sct',
                'code': '301000119104',  # SNOMED code for Pregnancy Status
                'display': 'Pregnancy Status',
            }
        ]
    })

    observation.subject = FHIRReference({'reference': f'Patient/{patient_id}'})

    observation.valueCodeableConcept = CodeableConcept({
        'coding': [
            {
                'system': 'http://snomed.info/sct',
                'code': '246075003',  # SNOMED code for Pregnant
                'display': 'Pregnant',
            }
        ]
    })

    observation.status = 'final'

    return observation


def create_observations_and_conditions(patient_id: str, observation_text: str):
    """Create FHIR Observations and Conditions based on the observation text."""
    resources = []

    if 'Gestante' in observation_text:
        save_observation(create_pregnancy_observation(patient_id), patient_id)
        resources.append(create_pregnancy_observation(patient_id))

    if 'Diabético' in observation_text:
        save_condition(create_diabetes_condition(patient_id), patient_id)
        resources.append(create_diabetes_condition(patient_id))

    if 'Hipertenso' in observation_text:
        save_condition(create_hypertension_condition(patient_id), patient_id)
        resources.append(create_hypertension_condition(patient_id))

    return resources


def save_resource(resource) -> str | None:
    """Save a FHIR resource to the server and return the assigned ID."""
    response = resource.create(fhir_client.server)
    if response:
        return response.get('id', None)
    return None


def save_patient(patient: Patient) -> str | None:
    """Save a FHIR Patient resource and return the assigned ID."""
    return save_resource(patient) or None


def save_observation(observation: Observation, patient_id: str) -> str | None:
    """Save a FHIR Observation resource and return the assigned ID."""
    observation.subject = FHIRReference({'reference': f'Patient/{patient_id}'})
    return save_resource(observation) or None


def save_condition(condition: Condition, patient_id: str) -> str | None:
    """Save a FHIR Condition resource and return the assigned ID."""
    condition.subject = FHIRReference({'reference': f'Patient/{patient_id}'})
    return save_resource(condition) or None


def map_to_fhir_patient_from_json(patient_csv: PatientCsv) -> Patient:
    """Map PatientCsv to FHIR Patient resource using JSON."""
    resources = None
    patient_json = patient_csv_to_json(patient_csv)

    fhir_patient = Patient.with_json(patient_json)

    patient_id = save_patient(fhir_patient)

    if not patient_id:
        raise Exception('Failed to save patient')

    if patient_csv.observation:
        resources = create_observations_and_conditions(
            patient_id, patient_csv.observation
        )

    pprint.pprint(resources)

    if resources is not None:
        pprint.pprint(resources[0].as_json())

    return fhir_patient


def proccess_patient(patient):
    return map_to_fhir_patient_from_json(normalize_patient(patient))

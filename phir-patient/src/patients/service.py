"""Functions for processing Patient data and saving FHIR resources."""

import asyncio

from fhirclient.models.condition import Condition
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.observation import Observation
from fhirclient.models.patient import Patient

from .fhir_client import fhir_client
from .models import (
    create_diabetes_condition,
    create_hypertension_condition,
    create_pregnancy_observation,
)
from .utils import normalize_patient, patient_csv_to_json


async def map_to_fhir_patient_from_json(patient_csv) -> Patient:
    """Map PatientCsv to FHIR Patient resource using JSON."""
    patient_json = patient_csv_to_json(patient_csv)
    fhir_patient = Patient.with_json(patient_json)
    patient_id = await save_patient(fhir_patient)

    if not patient_id:
        raise Exception('Failed to save patient')

    if patient_csv.observation:
        await create_observations_and_conditions(
            patient_id, patient_csv.observation
        )

    return fhir_patient


async def create_observations_and_conditions(
    patient_id: str, observation_text: str
):
    """Create FHIR Observations and Conditions based on the observation text."""
    tasks = []
    if 'Gestante' in observation_text:
        tasks.append(create_pregnancy_observation(patient_id))

    if 'Diabético' in observation_text:
        tasks.append(create_diabetes_condition(patient_id))

    if 'Hipertenso' in observation_text:
        tasks.append(create_hypertension_condition(patient_id))

    if tasks:
        await asyncio.gather(*tasks)


async def save_resource(resource) -> str | None:
    """Save a FHIR resource to the server and return the assigned ID."""
    response = await asyncio.to_thread(resource.create, fhir_client.server)
    if response:
        return response.get('id', None)
    return None


async def save_patient(patient: Patient) -> str | None:
    """Save a FHIR Patient resource and return the assigned ID."""
    return await save_resource(patient) or None


async def save_observation(
    observation: Observation, patient_id: str
) -> str | None:
    """Save a FHIR Observation resource and return the assigned ID."""
    observation.subject = FHIRReference({'reference': f'Patient/{patient_id}'})
    return await save_resource(observation) or None


async def save_condition(condition: Condition, patient_id: str) -> str | None:
    """Save a FHIR Condition resource and return the assigned ID."""
    condition.subject = FHIRReference({'reference': f'Patient/{patient_id}'})
    return await save_resource(condition) or None


async def process_patient(patient):
    """Process and save a patient and associated conditions."""
    patient_csv = normalize_patient(patient)
    patient_fhir = await map_to_fhir_patient_from_json(patient_csv)
    print(patient_fhir.as_json())
    return patient_fhir

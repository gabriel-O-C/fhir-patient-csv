"""Functions for creating FHIR resources."""

from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.condition import Condition
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.observation import Observation


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
    return condition


def create_hypertension_condition(patient_id: str) -> Condition:
    """Create a FHIR Condition resource for hypertension."""
    condition = Condition()
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
                'code': '301000119104',
                'display': 'Pregnancy Status',
            }
        ]
    })
    observation.subject = FHIRReference({'reference': f'Patient/{patient_id}'})
    observation.valueCodeableConcept = CodeableConcept({
        'coding': [
            {
                'system': 'http://snomed.info/sct',
                'code': '246075003',
                'display': 'Pregnant',
            }
        ]
    })
    observation.status = 'final'
    return observation

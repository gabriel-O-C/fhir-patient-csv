"""FHIR client configuration and initialization."""

from fhirclient import client

from src.patients.settings import SETTINGS

fhir_client = client.FHIRClient(SETTINGS)

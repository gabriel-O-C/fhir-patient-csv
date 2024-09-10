"""FHIR client configuration and initialization."""

from fhirclient import client

from .settings import SETTINGS

fhir_client = client.FHIRClient(SETTINGS)

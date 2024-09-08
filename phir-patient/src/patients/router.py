import asyncio
import csv
from http import HTTPStatus
from io import StringIO
from typing import Dict, List

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.patients.service import process_patient

router = APIRouter(prefix='/api/v1', tags=['patients'])


async def process_csv(file: UploadFile) -> List[Dict[str, str]]:
    """Read CSV file asynchronously and return list of dictionaries."""
    data = []
    try:
        contents = await file.read()
        try:
            reader = csv.DictReader(StringIO(contents.decode('utf-8')))
        except UnicodeDecodeError:
            reader = csv.DictReader(StringIO(contents.decode('latin-1')))

        for row in reader:
            data.append(row)
        return data
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post('/patients', status_code=HTTPStatus.CREATED)
async def create_patients(file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid file type'
        )

    patients = await process_csv(file)
    tasks = [process_patient(patient) for patient in patients]
    await asyncio.gather(*tasks)

    return {
        'message': 'Successfully created patients',
    }

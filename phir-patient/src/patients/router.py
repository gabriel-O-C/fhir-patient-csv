import csv
from http import HTTPStatus
from io import StringIO

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.patients.service import process_patient

router = APIRouter(prefix='/api/v1', tags=['patients'])


def parse_csv(file: UploadFile):
    if file.content_type != 'text/csv':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid file type'
        )
    try:
        contents = file.file.read()
        try:
            decoded_content = contents.decode('utf-8')
        except UnicodeDecodeError:
            decoded_content = contents.decode('latin-1')
        csv_data = StringIO(decoded_content)
        csv_reader = csv.DictReader(csv_data)
        patients_list = [row for row in csv_reader]

        patients_parsed = [
            process_patient(patient) for patient in patients_list
        ]
        return patients_list

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post('/patients', status_code=HTTPStatus.CREATED)
def create_patients(file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid file type'
        )

    patients_list = parse_csv(file)

    return {
        'message': 'Successfully created patients',
        'patients': patients_list,
    }

from fastapi import APIRouter, HTTPException, UploadFile, File
from http import HTTPStatus
import csv
from io import StringIO

router = APIRouter(prefix="/api/v1", tags=["patients"])


@router.post("/patients", status_code=HTTPStatus.CREATED)
async def create_patients(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid file type"
        )

    try:
        contents = file.file.read()
        try:
            decoded_content = contents.decode("utf-8")
        except UnicodeDecodeError:
            decoded_content = contents.decode("latin-1")

        csv_data = StringIO(decoded_content)
        csv_reader = csv.DictReader(csv_data)

        patients_list = [row for row in csv_reader]
        return {"message": "Successfully created patients", "patients": patients_list}

    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))

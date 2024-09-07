from http import HTTPStatus
from io import BytesIO

from fastapi import UploadFile


def make_request(file: UploadFile, client):
    response = client.post(
        '/api/v1/patients',
        files={
            'file': (
                file.filename,
                file.file,
            )
        },
    )
    return response


def create_upload_file(content: bytes, filename='test.csv'):
    return UploadFile(filename=filename, file=BytesIO(content))


def test_create_patients_success(client):
    file = create_upload_file(b'name,age\nJohn,30\nDoe,25')

    response = make_request(file, client)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'message': 'Successfully created patients',
        'patients': [
            {'name': 'John', 'age': '30'},
            {'name': 'Doe', 'age': '25'},
        ],
    }


def test_create_patients_invalid_file_type(client):
    file = create_upload_file(b'not_a_csv_content', filename='test.txt')

    response = make_request(file, client)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Invalid file type'


def test_create_patients_with_encoding_error(client):
    file = create_upload_file(
        b'\xea\xbc\xae\xea\xbc', filename='invalid_encoding.csv'
    )

    response = make_request(file, client)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'message': 'Successfully created patients',
        'patients': [],
    }


def test_create_patients_with_empty_file(client):
    file = create_upload_file(b'', filename='empty.csv')

    response = make_request(file, client)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'message': 'Successfully created patients',
        'patients': [],
    }

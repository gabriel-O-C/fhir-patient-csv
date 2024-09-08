from dataclasses import dataclass

key_mapping = {
    'Nome': 'name',
    'CPF': 'cpf',
    'Data de Nascimento': 'birth_date',
    'Gênero': 'gender',
    'Telefone': 'phone',
    'País de Nascimento': 'country',
    'Observação': 'observation',
}


@dataclass
class PatientCsv:
    name: str
    cpf: str
    birth_date: str
    gender: str
    phone: str
    country: str
    observation: str

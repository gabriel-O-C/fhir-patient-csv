# Desafio técnico munai

## Objetivo
Construir uma api que recebe um csv com dados de pacientes e processar eles para o sistema FHIR.

## Requisitos
- O sistema deve receber um csv com os dados de pacientes.
- O sistema deve processar os dados e criar um objeto do tipo `Patient` no sistema FHIR.
  - Caso exista um paciente com uma condição  como diabetes, o sistema deve criar um `Observation` e vincular o `Patient` ao `Observation`.
- O sistema deve armazenar os dados processados de forma asincrona em um banco de dados.


## Descrição da API
- O sistema recebe um csv com os dados de pacientes, no endpoint `api/v1/patients`.


## Como utilizar
- Para subir o sistema, basta executar o comando `docker-compose up` no terminal.
- Para utilizar o sistema, basta fazer um POST para o endpoint `api/v1/patients` com o csv com os dados de pacientes.

Exemplo:
```
curl -X POST http://localhost:8000/api/v1/patients -F "file=@/path/to/file.csv"
```

## Documentação da API
- Após subir o sistema, o Swagger está disponível em [http://localhost:8000/docs](http://localhost:8000/docs).

## Documentação do FHIR server
- [FHIR server](http://localhost:8080/fhir/)

## Como testar
Para testar o sistema, basta executar o comando `pytest` no terminal.


---
## Decisões de design e arquitetura
### Arquitetura
1. Primeiramente, resolvi desenvolver o sistema sem async, para que possa testar o código, e ver se a arquitetura permite que o sistema seja facilmente refatorado para usar async ou algum outro tipo de abordagem.
2. Após refatorar o sistema para async, me peguei pensando se faria sentido implementar rabbitmq para processar cada paciente de forma assíncrona. Mas, como nao tenho informações o suficiente sobre o estresse que o sistema precisa aguentar, decidi não implementar rabbitmq. E sim utilizar o asyncio.

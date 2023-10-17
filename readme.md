## Before start install poetry
`pip install poetry`

## Preparing venv
Run comands in project folder
`poetry install`

`poetry shell`

Create file `.env` with constants from `.env_template` 

## For run test
poetry run daphne -b 10.50.33.61 -p 8000 huawei_dj.asgi:application

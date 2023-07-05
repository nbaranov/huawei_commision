C:
cd C:\Users\NiVBaranov\Documents\code\huawei_commision
poetry install
poetry run daphne -b 10.50.33.61 -p 8000 huawei_dj.asgi:application
pause
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install bs4 matplotlib mysql-connector-python requests

CMD ["python", "./crypto_scrap.py"]

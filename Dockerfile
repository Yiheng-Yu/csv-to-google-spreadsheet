FROM python:3.13-slim

COPY requirements.txt .
COPY importer.py .

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "/importer.py"]

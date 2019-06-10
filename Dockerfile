FROM python:3.7-slim

COPY ./python /code
WORKDIR /code

RUN pip install --no-cache-dir -r requirements.txt \
    pip install -e .

ENTRYPOINT python ./mypackage/run.py

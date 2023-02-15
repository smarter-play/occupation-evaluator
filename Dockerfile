FROM python:3.11

WORKDIR /code
COPY src .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "src/webservice.py" ]

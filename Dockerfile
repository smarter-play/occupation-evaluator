FROM python:3.9

WORKDIR /code
COPY src .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "webservice.py" ]

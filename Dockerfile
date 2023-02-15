FROM python:3.11

WORKDIR /code
COPY src/weather.py weather.py
COPY src/db.py db.py
COPY src/occupation.py occupation.py
COPY src/occupation_forecast.py occupation_forecast.py
COPY src/webservice.py webservice.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "webservice.py" ]

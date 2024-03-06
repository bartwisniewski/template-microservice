FROM python:3.11-slim

WORKDIR /app

COPY ./deployment/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./gateproj /app/
COPY ./deployment/scripts/ /scripts

ENV PATH="/scripts::$PATH"

CMD ["run.sh"]

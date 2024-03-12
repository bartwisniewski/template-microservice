FROM python:3.9
WORKDIR /code/app
COPY ./deployment/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./frontjpy /code/app
CMD ["uvicorn", "main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

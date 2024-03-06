FROM python:3.9
WORKDIR /code
COPY ./deployment/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./booksapp /code/app
CMD ["uvicorn", "app.main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

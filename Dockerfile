FROM python:3.10

ENV MONGO_DB_USERNAME=admin \
    MONGO_DB_PWD=password

RUN mkdir -p /code/backend

WORKDIR /code/backend

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./backend /code/backend

CMD ["python", "main.py"]


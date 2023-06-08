FROM python:3.9-alpine3.13

ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip

COPY . .

WORKDIR .

RUN pip install -r requirements.txt && \
    python manage.py migrate

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
FROM python:3.9-alpine3.13

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt && \
    python manage.py makemigrations && \
    python mange.py migrate

EXPOSE 8000

CMD ["python","manage.py","runserver"]
FROM python:3.11-slim

WORKDIR /code

COPY . .

RUN pip install --no-cache --upgrade -r requirements.txt

# RUN ["python", "manage.py", "makemigrations", "crawler"]

# RUN ["python", "manage.py", "migrate"]

ENV DJANGO_PORT 8000

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

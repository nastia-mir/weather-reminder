FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ../backend .

EXPOSE 8000

CMD ["py", "manage.py", "makemigrations"]
CMD ["py", "manage.py", "migrate"]
CMD ["py", "manage.py", "runserver"]
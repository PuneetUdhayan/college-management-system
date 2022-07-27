FROM python:3.7

ADD requirements.txt requirements.txt
ADD setup_db.py setup_db.py

EXPOSE 8000

COPY ./app /app

CMD ["start.sh"]
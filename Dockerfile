FROM python:3.7

ADD requirements.txt requirements.txt
ADD start.sh start.sh

COPY ./app /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "start.sh"]
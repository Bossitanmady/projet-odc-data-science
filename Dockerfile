FROM python:3.12.4-slim 

WORKDIR /app 

COPY . /app

RUN pip install -r requirements.txt 

EXPOSE 80

CMD uvicorn app:app --host 0.0.0.0 --port $PORT 
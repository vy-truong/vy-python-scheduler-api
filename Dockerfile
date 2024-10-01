# FROM python:3.9-slim

# WORKDIR /app

# COPY ./app/requirements.txt /app/

# RUN pip install -r requirements.txt

# RUN apt-get update && apt-get install -y curl

# COPY ./app /app

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

FROM python:3.9-slim

WORKDIR /app

COPY ./app/requirements.txt /app/

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y curl

COPY ./app /app
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

CMD ["./wait-for-db.sh", "db", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

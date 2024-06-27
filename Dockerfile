FROM python:3.8.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
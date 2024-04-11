FROM python:3.11


COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -yq \
chromium-driver

CMD ["python", "main.py"]


FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install Flask pytz requests

# EXPOSE is optional and used for documentation purposes
EXPOSE 53533/udp

CMD ["python", "AS.py"]

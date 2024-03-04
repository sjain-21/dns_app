FROM python:3.8-slim

WORKDIR /app

COPY AS.py /app/AS.py

RUN pip install socket

EXPOSE 53533/udp

CMD ["python", "AS.py"]

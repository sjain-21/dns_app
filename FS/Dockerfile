FROM python:3.10-slim


WORKDIR /app-dir


COPY . /app-dir


RUN pip install --no-cache-dir Flask==2.0.2

EXPOSE 9090


CMD ["python3", "FS.py"]

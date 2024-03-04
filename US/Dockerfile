FROM python:3.10-slim


RUN apt-get update && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN groupadd -g 900 appgroup && useradd -m -r -u 1001 -g appgroup appuser


WORKDIR /application-dir

COPY . .

RUN pip install --no-cache-dir Flask==2.0.2 requests==2.26.0


USER appuser


COPY --chown=appuser:appgroup . .


CMD ["python3", "US.py"]

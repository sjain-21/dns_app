FROM python:3.10


RUN apt-get update && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN groupadd -g 900 appgroup && useradd -r -u 1000 -g appgroup appuser


WORKDIR /application

COPY . .


RUN pip install --no-cache-dir Flask==2.0.2


USER appuser


CMD [ "python3", "./AS.py" ]

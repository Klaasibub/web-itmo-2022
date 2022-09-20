FROM python:3.8-slim

WORKDIR /

COPY ./requirements.txt requirements.txt
COPY ./entrypoint.sh entrypoint.sh

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src ./src

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]

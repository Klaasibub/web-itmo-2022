FROM python:3.8-slim

WORKDIR /

COPY ./requirements/prod.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh ./pyproject.toml /
COPY ./migrations/ /migrations

COPY ./src ./src

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]

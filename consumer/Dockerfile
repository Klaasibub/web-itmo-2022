FROM python:3.8-slim

WORKDIR /

COPY ./requirements/prod.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /consumer

COPY ./consumer /consumer

ENTRYPOINT ["python3", "-u", "main.py"]

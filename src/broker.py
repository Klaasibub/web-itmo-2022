import logging

import pika
import pika.exceptions

from retry import retry

from settings import BROKER_USER, BROKER_PASSWORD, BROKER_HOST, LOG_FORMAT


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT)


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def send_msg(queue: str, body: str):
    credentials = pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD)
    parameters = pika.ConnectionParameters(BROKER_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=queue, body=body)
    connection.close()

import json
import pika
import retry
from time import sleep
import smtplib
from email.mime.text import MIMEText

from settings import BROKER_USER, BROKER_PASSWORD, BROKER_HOST, DEFAULT_QUEUE, MAILCATCHER_HOST, MAILCATCHER_PORT


def on_message(channel, method_frame, header_frame, body, userdata=None):
    task_body = json.loads(body)
    from_email = task_body['from']
    to_email = task_body['to']
    subject = task_body['subject']
    msg = MIMEText(task_body['msg'])

    sleep(len(subject) * 0.1)

    s = smtplib.SMTP(MAILCATCHER_HOST, MAILCATCHER_PORT)
    # s.login("guest", "guest")
    s.sendmail(from_email, [to_email], msg.as_string())
    s.quit()

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


# @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def consume():
    credentials = pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD)
    parameters = pika.ConnectionParameters(BROKER_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue=DEFAULT_QUEUE)
    channel.basic_consume(DEFAULT_QUEUE, on_message)

    try:
        channel.start_consuming()
    # Don't recover connections closed by server
    except pika.exceptions.ConnectionClosedByBroker:
        pass

    connection.close()


if __name__ == '__main__':
    consume()

import sys
import time
from RabbitMQ import channel, connection
import pika


def callback(ch, method, properties, body):
    print(" [x] %r" % body)

def route_mothed():
    channel.exchange_declare(exchange='logs2',
                             exchange_type='direct')

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    severities = ["info11", "warning", "error"]

    # 创建多个关键字
    for severity in severities:
        channel.queue_bind(exchange='logs2',
                           queue=queue_name,
                           routing_key=severity  # 关键字
                           )

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(queue=queue_name,
                          auto_ack=True,
                          on_message_callback=callback)

    channel.start_consuming()

if __name__ == '__main__':
    route_mothed()
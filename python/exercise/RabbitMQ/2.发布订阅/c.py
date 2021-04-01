import time

from RabbitMQ import channel, connection
import pika


def callback(ch, method, properties, body):
    print(" [x] %r" % body)

def dingyue():
    # 声明交换机，防止消费者先启动而找不到交换机
    channel.exchange_declare(exchange='logs',
                             exchange_type='fanout')
    # 创建队列
    result = channel.queue_declare("",exclusive=True) # 创建随机的队列
    queue_name = result.method.queue # 获取队列名字
    # 将指定队列绑定到交换机上
    channel.queue_bind(exchange='logs',
                       queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(queue=queue_name,
                          auto_ack=True,
                          on_message_callback=callback)

    channel.start_consuming()

if __name__ == '__main__':
    dingyue()
from RabbitMQ import channel, connection
import pika
# 路由模式
def route():
    channel.exchange_declare(exchange='logs2',
                             exchange_type='direct')

    message = "info: Hello Yuan!"
    channel.basic_publish(exchange='logs2',
                          routing_key='info11',  # 关键字
                          body=message)
    print(" [x] Sent %r" % message)
    connection.close()

if __name__ == '__main__':
    route()
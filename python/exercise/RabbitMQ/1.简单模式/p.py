from RabbitMQ import channel, connection
import pika
def jiandanmoshi(msg):
    # 2.创建队列
    channel.queue_declare(queue='hello')
    # 3.向指定队列插入数据
    channel.basic_publish(exchange='',  # 1.简单模式
                          routing_key='hello',  # 指定队列
                          body='Hello World!{}'.format(msg))  # 数据

    print(" [x] Sent 'Hello World!'{}".format(msg) )
    # connection.close()
if __name__ == '__main__':
    msg = 1
    while 1:
        jiandanmoshi(msg)
        msg+=1
import time

from RabbitMQ import channel, connection
import pika

# 一直发信息
def fabu_always():
    # channel.exchange_declare(exchange='logs',  # 交换机名称
    #                          exchange_type='fanout'  # 模式 发布订阅
    #                          )
    x = 1
    while True:
        # time.sleep(.3)
        message = "info: Hello World 这是我生成的一个任务你来完成它2222222222 {}!".format(x)
        # 向logs交换机插入数据
        channel.basic_publish(exchange='logs',
                              routing_key='',  # 不涉及到关键字所以这里为空
                              body=message)
        print(" [x] Sent %r" % message)
        x += 1

if __name__ == '__main__':
    fabu_always()
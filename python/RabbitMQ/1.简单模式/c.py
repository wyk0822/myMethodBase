import time
from python.RabbitMQ import channel
import pika
# 回掉函数，使用队列中的数据
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def callback_Notauto(ch, method, properties, body):
    print(body)
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag) # 手动应答
    print("callback_Notauto: ", body)

def auto():
    # 创建队列， 避免生产者后启动而找不到队列
    channel.queue_declare(queue='hello')


    # 确定监听队列参数
    channel.basic_consume(queue='hello', # 监听hello队列
                          auto_ack=True, # 默认应答, 取出数据队列中就会消失
                          on_message_callback=callback # 回调
                          )


    print(' [*] Waiting for messages. To exit press CTRL+C')
    # 正式监听
    channel.start_consuming()

def NotAuto():
    # 创建队列， 避免生产者后启动而找不到队列
    channel.queue_declare(queue='hello')
    # 争抢模式先完成就先拿数据
    channel.basic_qos(prefetch_count=1)

    # 确定监听队列参数
    channel.basic_consume(queue='hello',  # 监听hello队列
                          auto_ack=False,  # 默认应答, 取出数据队列中就会消失
                          on_message_callback=callback_Notauto  # 回调
                          )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # 正式监听
    channel.start_consuming()

if __name__ == '__main__':
    NotAuto()

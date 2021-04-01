import pika  # 连接模块

# 1.创建连接对象
Credentials = pika.PlainCredentials("guest", "guest")  # 创建认证信息对象
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', '5672', '/', Credentials))

channel = connection.channel()
# # 2.创建队列
# channel.queue_declare(queue='hello')
# # 3.向指定队列插入数据
# channel.basic_publish(exchange='',  # 1.简单模式
#                       routing_key='hello',  # 指定队列
#                       body='Hello World!')  # 数据
#
# print(" [x] Sent 'Hello World!'" )

# -*- coding:utf-8 -*-

#
# class RabbitMQ(object):
#     """一个简单的RabbitMQ的库，为了学习pika库"""
#
#     def __init__(self, host='127.0.0.1', port=5672, username=None, password=None):
#         """
#             创建RabbitMQ的一个简单连接发起对象，参数如下
#             （1）配置host，也就是RabbitMQ的IP地址.默认是127.0.0.1；
#             （2）配置port，也就是RabbitMQ的端口信息，默认是5672；
#             （3）可以配置用户名username、口令password，默认是None。
#         """
#         if username != None and password != None:
#             try:
#                 self.Credentials = pika.PlainCredentials(username, password)  # 创建认证信息对象
#                 self.ConnectionKeys = pika.ConnectionParameters(host, port, '/', self.Credentials)  # 根据认证信息对象创建连接函数参数
#             except Exception:
#                 raise
#         else:
#             self.ConnectionKeys = None
#
#     def _connection(self):
#         """发起连接的函数"""
#         try:
#             if self.ConnectionKeys == None:
#                 self.connection = pika.BlockingConnection()  # 无配置信息的连接
#             else:
#                 self.connection = pika.BlockingConnection(self.ConnectionKeys)  # 有配置信息的连接
#         except Exception:
#             raise
#
#     def _channel(self):
#         """创建频道（游标）的函数"""
#         self.channel = self.connection.channel()  # 创建频道（游标）
#
#     def _callback(channel, method, properties, body):
#         """callback函数，返回body体"""
#         print
#         "[+] Received Message:%s" % body
#
#     def connect(self):
#         """实例调用的连接接口"""
#         self._connection()
#         self._channel()
#
#     def create_queque(slef, flag, durableflag=False):
#         """创建一个新队列，flag是队列名称，durablflag是是否永久化的标志位，True表示永久化，False表示不是永久化"""
#         try:
#             self.channel.queue_declare(queue=flag, durable=durableflag)  # 创建新的消息队列
#         except Exception:
#             raise
#
#     def set_queue_number(count):
#         try:
#             self.channel.basic_qos(prefetch_count=count)  # 每个worker每次count个消息
#         except Exception:
#             raise
#
#     def commit(self):
#         """确认函数"""
#         try:
#             self.channel.basic_ack(delivery_tag=method.delivery_tag)  # 回发确认报文
#         except Exception:
#             raise
#
#     def
#         def product(self, flag, content, exchange=''):
#             """生产消息，flag是消息队列名称，content是消息队列内容"""
#             try:
#                 self.channel.basic_publish(exchange='', routing_key=flag, body=content)  # 发送消息进入消息队列
#             except Exception:
#                 raise
#
#     def consume(slef, funcname=self._callback, flag, ackflag):
#         """消费消息，flag是队列名称，ackflag是no_ack的标志位，True代表消息确认关闭"""
#         """
#             消息确认，是指在consumer收到一个消息但是还没有处理完成就死掉了的情况下，这个消息会回到消息队列里；
#         """
#         try:
#             self.channel.basic_consume(callback=funcname, queue=flag, no_ack=ackflag)  # 从队列获取消息
#         except Exception:
#             raise
#
#     def close(self):
#         """关闭连接"""
#         try:
#             self.connection.close()  # 关闭连接
#         except Exception:
#             raise
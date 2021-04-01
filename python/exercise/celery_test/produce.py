# -*- coding: utf-8 -*-
from celery_task.task01 import send_email
from celery_task.task02 import send_msg
import time
x = 1
# 立即告知celery去执行test_celery任务，并传入一个参数
result = send_email.delay('第{}个任务'.format(x))
print(result.id)
# result = send_msg.delay('yuan')
# print(result.id)

# with open("res_id.txt", "a+") as f:
#     while 1:
#         result = send_email.delay('第{}个任务'.format(x))
#         print(result.id)
#         f.write(result.id+"\n")
#         print(x)
#         x+=1









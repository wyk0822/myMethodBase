import time
from .celery import cel


@cel.task
def send_email(res):
    print(res)
    # time.sleep(.1)
    return "完成向%s发送邮件任务"%res
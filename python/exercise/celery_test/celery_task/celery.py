from __future__ import absolute_import, unicode_literals
from celery import Celery

cel = Celery(__name__,
             broker='amqp://guest@127.0.0.1:5672',
             backend='redis://127.0.0.1:6379/6',
             # 包含以下两个任务文件，去相应的py文件中找任务，对多个任务做分类
             include=['celery_task.task01',
                      'celery_task.task02'
                      ],
            task_reject_on_worker_lost = True,
            task_acks_late = True
            )

# 时区
cel.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
cel.conf.enable_utc = False

# cel.conf.task_reject_on_worker_lost = True
# cel.conf.task_acks_late = True
# task_reject_on_worker_lost作用是当worker进程意外退出时，task会被放回到队列中
# task_acks_late作用是只有当worker完成了这个task时，任务才被标记为ack状态

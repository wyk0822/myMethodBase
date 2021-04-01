import os

file_path = os.path.abspath(os.path.dirname(__file__))

class Config:
    """ Base configuration"""
    SECRET_KEY = "5f3523l9324cy2463s51387a0aec5d2f"

    # db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/.sqlite.db'.format(file_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # celery
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/9'
    CELERY_BROKER_URL = 'amqp://guest@192.168.1.28:5672'
    # 每个worker执行1个任务后销毁重建
    CELERYD_MAX_TASKS_PER_CHILD = 1
    # 防止死锁
    CELERYD_FORCE_EXECV = True

    # 上传文件大小限制 2M
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
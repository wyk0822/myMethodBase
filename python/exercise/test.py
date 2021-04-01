import threading
import random

class UserManager(object):
    # 定义静态变量实例
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        print(13221)

    def __new__(cls, *args, **kwargs):
        print(cls.__instance)
        if cls.__instance == None:
            # print(cls.__instance)
            try:
                UserManager.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = 1
            finally:
                UserManager.__lock.release()
        return cls.__instance


# user_manager = UserManager()
#
# print(user_manager)
# print("----------------")
# a = UserManager()
# print(a)


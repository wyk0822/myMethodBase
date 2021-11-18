#连接redis
import time
import uuid
from threading import Thread

import pymysql
import redis

redis_client = redis.Redis(host="localhost",
                           port=6379,
                           # password=123456,
                           db=10)

#获取一个锁
# lock_name：锁定名称
# acquire_time: 客户端等待获取锁的时间
# time_out: 锁的超时时间
def acquire_lock(lock_name, acquire_time=10, time_out=10):
    """获取一个分布式锁"""
    identifier = str(uuid.uuid4())
    end = time.time() + acquire_time
    lock = "string:lock:" + lock_name
    while time.time() < end:
        # setnx(key,value) 只有key不存在情况下，将key的值设置为value，若key存在则不做任何动作,返回True和False
        if redis_client.setnx(lock, identifier):
            # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
            redis_client.expire(lock, time_out)
            return identifier
        # 当锁未被设置过期时间时，重新设置其过期时间
        elif not redis_client.ttl(lock):
            redis_client.expire(lock, time_out)
        time.sleep(0.001)
    return False

#释放一个锁
def release_lock(lock_name, identifier):
    """通用的锁释放函数"""
    lock = "string:lock:" + lock_name
    pip = redis_client.pipeline(True)
    while True:
        try:
            # 通过watch命令监视某个键，当该键未被其他客户端修改值时，事务成功执行。当事务运行过程中，发现该值被其他客户端更新了值，任务失败
            pip.watch(lock)
            lock_value = redis_client.get(lock) # 检查客户端是否仍然持有该锁
            if not lock_value:
                return True

            if lock_value.decode() == identifier:
                # multi命令用于开启一个事务，它总是返回ok
                # multi执行之后， 客户端可以继续向服务器发送任意多条命令， 这些命令不会立即被执行， 而是被放到一个队列中， 当 EXEC 命令被调用时， 所有队列中的命令才会被执行
                pip.multi()
                # 删除键，释放锁
                pip.delete(lock)
                # execute命令负责触发并执行事务中的所有命令
                pip.execute()
                return True
            pip.unwatch()
            break
        except redis.WatchError:
            # 释放锁期间，有其他客户端改变了键值对，锁释放失败，进行循环
            pass
    return False

count=10

def seckill(i):
    identifier=acquire_lock('resource', 10)
    if identifier:
        print("线程:{}--获得了锁{}\t".format(i, identifier))
        global count
        if count<1:
            print("线程:{}--没抢到，票抢完了\t".format(i))
            release_lock('resource', identifier)
            return
        time.sleep(1)
        count-=1
        print("线程:{}--抢到一张票，还剩{}张票\t".format(i,count))
        release_lock('resource',identifier)
    else:
        print("等待超时")

def saveToMysql(i, timeout=1):
    print(f"线程{i}开始")
    mysql_client = pymysql.connect(host='192.168.58.216',
                                   user='root',
                                   password='123456',
                                   database='test')
    cur = mysql_client.cursor()
    cur.execute(f"INSERT INTO test(name)VALUES ('{i}')")
    time.sleep(timeout)
    mysql_client.commit()
    mysql_client.close()
    print(f"线程{i}结束")

def del_table(tableName):
    mysql_client = pymysql.connect(host='192.168.58.216',
                                   user='root',
                                   password='123456',
                                   database='test')
    cur = mysql_client.cursor()
    try:
        cur.execute(f"DROP TABLE {tableName};")
        cur.execute(f"CREATE TABLE {tableName} (id INT NOT NULL AUTO_INCREMENT, name INT NULL,  PRIMARY KEY (`id`));")
        mysql_client.commit()
        print(f'成功重新创建数据库{tableName}')
    except:
        print("出现错误回滚")
        mysql_client.rollback()
    finally:
        mysql_client.close()
def update(i, id, timeout):
    identifier = acquire_lock(f'{id}')
    if identifier:
        print("线程:{}--获得了锁\t".format(i))
    else:
        print(f"线程{i}--未获得锁")
        return
    print(f"线程{i}开始")
    mysql_client = pymysql.connect(host='192.168.58.216',
                                   user='root',
                                   password='123456',
                                   database='test')
    cur = mysql_client.cursor()
    cur.execute(f"SELECT * FROM test where id = {id};")
    data = cur.fetchone()[1]
    print(data, timeout)
    time.sleep(timeout)
    cur.execute(f"update test set name={data + 2} where id = {id}")
    mysql_client.commit()
    cur.execute(f"SELECT * FROM test where id = {id};")
    print(f"线程{i}执行后数值：{cur.fetchone()[1]}")
    mysql_client.close()
    release_lock(f'{id}', identifier)
    print(f"线程{i}结束")

if __name__ == '__main__':
    # del_table("test")
    # tlst = []
    # start = time.time()
    # for i in range(50):
    #     # saveToMysql(i, 1, i)
    #     # saveToMysql(i, 2, i)
    #     t = Thread(target=saveToMysql, args=(i,  ))
    #     t2 = Thread(target=saveToMysql, args=(i,  ))
    #     t.start()
    #     t2.start()
    #     tlst.append(t)
    #     tlst.append(t2)
    #
    #
    # for i in tlst:
    #     i.join()
    # print(time.time()-start)


    for i in range(50):
        t = Thread(target=seckill,args=(i,))
        t.start()

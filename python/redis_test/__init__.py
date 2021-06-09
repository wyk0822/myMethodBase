# -*- coding: UTF-8 -*-
# @author: wyk
# @file: update_server.py
# @time: 2021/04/19
# @Project: myMethodBase


#!/usr/bin/env python
#_*_ coding:UTF-8 _*_

import redis


####配置参数
host = '192.168.58.95'
port = 6379



####
#连接redis
#单个值的
def redis_conn(host,port,db,key,act="get",value=''):
    r = redis.StrictRedis(host=host, port=port,db=db, decode_responses=False)

    #判断key类型
    s = r.type(key)
    print('type of key: %s'%s)

    #设置key
    if act=="set":
            r.set(key,value)
            print('已经set完，db%s,key=%s,值为 %s'%(db,key,value))
            return value

    if r.exists(key):
        #查询
        if act=="get":
            # 取key值
            value=r.get(key)
            print('正在查询db%s,key=%s \n value=%s'%(db,key,value))
            return value

        #删除
        elif act=="del":
            # 取key值
            value=r.get(key)
            r.delete(key)
            print('已经删除，db%s,key=%s,\n值为 %s'%(db,key,value))
            return
    else:
        print('key 不存在')


key="old_user_pop_win_count_20190910_22"
db=2
#调用函数，get
result=redis_conn(host,port,db,key,act="get")
print('result:',result)

#del
result=redis_conn(host,port,db,key,act="del")
print('result:',result)


#set
db=1
key="age"
result=redis_conn(host,port,db,key,act="set",value="88")
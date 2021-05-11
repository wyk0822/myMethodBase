# # -*- coding: utf-8 -*-
# import sys
# import uuid
# import requests
# import hashlib
# import time
# # from imp import reload
#
# import time
#
# # reload(sys)
#
# YOUDAO_URL = 'https://openapi.youdao.com/api'
# APP_KEY = '15c5ab545a3d'
# APP_SECRET = 'jmG1acQ9FGVTCFI'
#
#
# def encrypt(signStr):
#     hash_algorithm = hashlib.sha256()
#     hash_algorithm.update(signStr.encode('utf-8'))
#     return hash_algorithm.hexdigest()
#
#
# def truncate(q):
#     if q is None:
#         return None
#     size = len(q)
#     return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]
#
#
# def do_request(data):
#     # 2、组织headers 发送post请求
#     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#     req:requests = requests.post(YOUDAO_URL, data=data, headers=headers)
#     return req
#
#
# def connect():
#     # 1、请求参数
#     q = "我"
#     data = {}
#     data['from'] = 'zh-CHS'
#     data['to'] = 'en'
#     data['signType'] = 'v3'
#     curtime = str(int(time.time()))
#     data['curtime'] = curtime
#     salt = str(uuid.uuid1())
#     signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
#     sign = encrypt(signStr)
#     data['appKey'] = APP_KEY
#     data['q'] = q
#     data['salt'] = salt
#     data['sign'] = sign
#     data['vocabId'] = "6992d5f18b5c11e4"
#
#     response = do_request(data)
#     contentType = response.headers['Content-Type']
#     if contentType == "audio/mp3":
#         millis = int(round(time.time() * 1000))
#         filePath = "./a" + str(millis) + ".mp3"
#         fo = open(filePath, 'wb')
#         fo.write(response.content)
#         fo.close()
#     else:
#         resp = response.content.decode()
#         print(response.headers)
#
#
#
# if __name__ == '__main__':
#     connect()




# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 10:15:37 2018

@author: python
"""


import json
import requests
import random

class youdao:
    def __init__(self):
        self.params = {
        'from':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':'1543198914021',
        'sign':'1eb94666d05e93f3221178d89ee7a583',
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_REALTIME',
        'typoResult':'false'
    }

        self.url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        self.h_list = [
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},
            {"User-Agent": "Mozilla/4.0"},
            {"User-Agent": "Mozilla/3.0"},
            {"User-Agent": "Mozilla/2.0"},
            {"User-Agent": "Mozilla/1.0"},
        ]
    def reqAip(self,text):
        self.params["i"] = text
        res = requests.post(self.url, data=self.params, headers=random.choice(self.h_list))
        res.encoding = "utf-8"
        html = res.text
        print(html)
        # html为json格式的字符串
        r_dict = json.loads(html)
        print(r_dict['translateResult'][0][0]['tgt'])

# key = input('要翻译的内容:')
# data = {
#         'i':key,
#         'from':'AUTO',
#         'to':'AUTO',
#         'smartresult':'dict',
#         'client':'fanyideskweb',
#         'salt':'1543198914021',
#         'sign':'1eb94666d05e93f3221178d89ee7a583',
#         'doctype':'json',
#         'version':'2.1',
#         'keyfrom':'fanyi.web',
#         'action':'FY_BY_REALTIME',
#         'typoResult':'false'
#     }
#
# url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
# h_list = [
#                 {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},
#                 {"User-Agent":"Mozilla/4.0"},
#                 {"User-Agent":"Mozilla/3.0"},
#                 {"User-Agent":"Mozilla/2.0"},
#                 {"User-Agent":"Mozilla/1.0"},
#             ]
# headers = random.choice(h_list)
#
# # 用post方式发送请求，data直接用字典格式
#
#
# res = requests.post(url,data=data,headers=headers)
#
# res.encoding = "utf-8"
# html = res.text
# # print(html)
#
# # html为json格式的字符串
# r_dict = json.loads(html)
# #print(r_dict)
# print(r_dict['translateResult'][0][0]['tgt'])

if __name__ == '__main__':
    yd = youdao()
    yd.reqAip("测试")









#1.把form表单数据整理成字典
#2、urlencode（字典） -> 字符串
#3、字符串.encode("utf-8") -> 字节流



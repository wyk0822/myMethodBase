# import asyncio
# async def others(c):
#     print(f"start{c}")
#     await asyncio.sleep(10)
#     print(f'end{c}')
#     return f'返回值{c}'
# async def func(c):
#     print(f"执行协程函数内部代码{c}")
#     # 遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续往下执行。当前协程挂起时，事件循环可以去执行其他协程（任务）。
#     response1 = await others(c)
#     print("IO请求结束，结果为：", response1)
#     response2 = await others(c)
#     print("IO请求结束，结果为：", response2)
#
# # for i in range(3):
# asyncio.run( func("2222") )
# asyncio.run( func("3333") )

# import asyncio
# async def others():
#     print("start")
#     await asyncio.sleep(2)
#     print('end')
#     return '返回值'
# async def func():
#     print("执行协程函数内部代码")
#     # 遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续往下执行。当前协程挂起时，事件循环可以去执行其他协程（任务）。
#     response = await others()
#     print("IO请求结束，结果为：", response)
# asyncio.run( func() )

# import asyncio
# async def func():
#     print(1)
#     await asyncio.sleep(2)
#     print(2)
#     return "返回值"
# async def main():
#     print("main开始")
#     # 创建协程，将协程封装到Task对象中并添加到事件循环的任务列表中，等待事件循环去执行（默认是就绪状态）。
#     # 在调用
#     task_list = [
#         asyncio.create_task(func(), name="f1"),
#         asyncio.create_task(func(), name='f2')
#     ]
#     print("main结束")
#     # 当执行某协程遇到IO操作时，会自动化切换执行其他任务。
#     # 此处的await是等待所有协程执行完毕，并将所有协程的返回值保存到done
#     # 如果设置了timeout值，则意味着此处最多等待的秒，完成的协程返回值写入到done中，未完成则写到pending中。
#     done, pending = await asyncio.wait(task_list, timeout=None)
#     print(list(done)[0].result(), pending)
#     print(type(list(done)[0]), pending)
# asyncio.run(main())


# import asyncio
# import requests
# async def download_image(url):
#     # 发送网络请求，下载图片（遇到网络下载图片的IO请求，自动化切换到其他任务）
#     print("开始下载:", url)
#     loop = asyncio.get_event_loop()
#     # requests模块默认不支持异步操作，所以就使用线程池来配合实现了。
#     future = loop.run_in_executor(None, requests.get, url)
#     response = await future
#     print('下载完成')
#     # 图片保存到本地文件
#     file_name = url.rsplit('_')[-1]
#     with open(file_name, mode='wb') as file_object:
#         file_object.write(response.content)
# if __name__ == '__main__':
#     url_list = [
#         'https://www3.autoimg.cn/newsdfs/g26/M02/35/A9/120x90_0_autohomecar__ChsEe12AXQ6AOOH_AAFocMs8nzU621.jpg',
#         'https://www2.autoimg.cn/newsdfs/g30/M01/3C/E2/120x90_0_autohomecar__ChcCSV2BBICAUntfAADjJFd6800429.jpg',
#         'https://www3.autoimg.cn/newsdfs/g26/M0B/3C/65/120x90_0_autohomecar__ChcCP12BFCmAIO83AAGq7vK0sGY193.jpg'
#     ]
#     tasks = [download_image(url) for url in url_list]
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete( asyncio.wait(tasks) )

# 使用多线程：在协程中集成阻塞io
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# import socket
# from urllib.parse import urlparse
#
#
# def get_url(url):
#     # 通过socket请求html
#     url = urlparse(url)
#     host = url.netloc
#     path = url.path
#     if path == "":
#         path = "/"
#
#     # 建立socket连接
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # client.setblocking(False)
#     client.connect((host, 80))  # 阻塞不会消耗cpu
#
#     # 不停的询问连接是否建立好， 需要while循环不停的去检查状态
#     # 做计算任务或者再次发起其他的连接请求
#
#     client.send(
#         "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))
#
#     data = b""
#     while True:
#         d = client.recv(1024)
#         if d:
#             data += d
#         else:
#             break
#
#     data = data.decode("utf8")
#     html_data = data.split("\r\n\r\n")[1]
#     print(html_data)
#     client.close()
#
#
# if __name__ == "__main__":
#     import time
#     start_time = time.time()
#     loop = asyncio.get_event_loop()
#     executor = ThreadPoolExecutor(3)
#     tasks = []
#     for url in range(20):
#         url = "http://shop.projectsedu.com/goods/{}/".format(url)
#         # 返回 task
#         task = loop.run_in_executor(executor, get_url, url)
#         tasks.append(task)
#     loop.run_until_complete(asyncio.wait(tasks))
#     print("last time:{}".format(time.time()-start_time))




class DataSet(object):
    def __init__(self):
        self._images = 1
        self._labels = 2 #定义属性的名称
    @property
    def images(self): #方法加入@property后，这个方法相当于一个属性，这个属性可以让用户进行使用，而且用户有没办法随意修改。
        return self._images
    @property
    def labels(self):
        return self._labels
    @images.setter
    def images(self, im):
        self._images = im
l = DataSet()
#用户进行属性调用的时候，直接调用images即可，而不用知道属性名_images，因此用户无法更改属性，从而保护了类的属性。
print(l.images) # 加了@property后，可以用调用属性的形式来调用方法,后面不需要加（）。
l.images = 10
print(l.images)
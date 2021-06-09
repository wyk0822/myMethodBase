# -*- coding: utf-8 -*-
# @Time    : 4/1/2019 19:27
# @Author  : MARX·CBR
# @File    : update_server.py
import pickle
from flask import request, jsonify, send_from_directory, abort, Flask, make_response
import os
import hashlib
import json

app = Flask(__name__, static_folder="abcd")
# allfile = []
# md5_list = []
# updateList = {}
directory = os.getcwd()

# 下载文件服务
@app.route("/<path:filename>", methods=['GET'])
def download(filename):
    folder = request.args.get("folder")
    print(os.path.join(folder, filename))
    if request.method == "GET":
        if os.path.isfile(os.path.join(folder, filename)):
            return send_from_directory(directory+f'/{folder}/', filename, mimetype='application/octet-stream',as_attachment=True)
        abort(404)



# 计算文件MD5
def Getfile_md5(filename):
    if not os.path.isfile(filename):
        return
    myHash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myHash.update(b)
    f.close()
    return myHash.hexdigest()


# 计算生成新的清单文件
@app.route("/generateNewConfig/<string:mac>/<string:folder>/", methods=['GET'])
def generate(mac, folder):
    filename = mac+"_listFile"
    updateList = {}
    # 找到更新文件目录里面的文件以及文件夹、递归寻找
    def findFile(path):
        fsinfo = os.listdir(path)
        for fn in fsinfo:
            temp_path = os.path.join(path, fn)
            if not os.path.isdir(temp_path):
                print('文件路径: {}'.format(temp_path))
                fm = Getfile_md5(temp_path)
                fn = temp_path.replace(directory + f"/{folder}/", '')
                print(os.path.getsize(temp_path.replace('\\', '/')), fn)
                # updateList[fn] = fm
                updateList[fn] = {"md5": fm, "size": os.path.getsize(temp_path.replace('\\', '/'))}
            else:
                findFile(temp_path)

    findFile(directory + f'/{folder}/')
    file_md5_list = json.dumps(updateList)
    print(file_md5_list)
    with open(f'./update_list_files/{filename}', 'wb') as f:
        pickle.dump(updateList, f)
    return_data = {
        'code': 0,
        'message': f'已生成更新清单，存放位置: update_list_files/{filename}'
    }
    return jsonify(return_data)
    # file_md5_list=json.load(updateList)



# 检查更新版本，该部分尚未够，完善。可以考虑为管理员远程上传文件的时候
# 将更新说明以json格式一同上传到服务器中，更新时直接读取即可
@app.route("/checkUpdate/<string:project>/<string:client_version>/", methods=['GET'])
def check(client_version, project):
    with open('version.json', "rb") as f:
        projectdata = json.load(f)
    status = version(projectdata[project]['version'], client_version)
    if status == 0:
        return_data = {
            "code":0,
            'Vresion': projectdata[project]['version'],
            'Msg': '当前已是最新版本，无需更新'
        }
    elif status == 1:
        return_data = {
            "code": 1,
            'Vresion': projectdata[project]['version'],
            'Msg': f'存在更新:{projectdata[project]["update_message"]}'
        }
    elif status == -1:
        return_data = {
            "code": -1,
            'Vresion': projectdata[project]['version'],
            'Msg': '客户端版本高于服务器版本'
        }
    else:
        return_data = {}
    return jsonify(return_data)

# 首页Hello
@app.route("/", methods=['GET'])
def hello():
    if request.method == "GET":
        return "Hello MARXCBR"


def version(v1, v2):
    """
    :param v1: 第一个版本号
    :param v2: 第二个版本号 两个版本号中只能包含数字和 "." 存在
    :return: 0表示v1=v2， 1表示v1>v2 , -1表示v1<v2
    """
    lst_1 = v1.split('.')
    lst_2 = v2.split('.')
    c = 0
    while True:
        if c == len(lst_1) and c == len(lst_2):
            return 0
        if len(lst_1) == c:
            lst_1.append(0)
        if len(lst_2) == c:
            lst_2.append(0)
        if int(lst_1[c]) > int(lst_2[c]):
            return 1
        elif int(lst_1[c]) < int(lst_2[c]):
            return -1
        c += 1

def mkdir(path):
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=1213, debug=True)  # 运行，指定监听地址为 127.0.0.1:8080

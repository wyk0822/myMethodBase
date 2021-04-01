# coding:utf-8
# 打开端口时会断开画面，需要重新连接
import os
import subprocess
from time import sleep


class Config:
    PHONEINFO = [
        {"devicesId": "HMKNW17909033816", "phoneName": "荣耀8青春版", "ip": "192.168.56.50"},
        {"devicesId": "JPFDU19222030922", "phoneName": "nova4", "ip": "192.168.57.23"}
    ]


def devices():
    devicesInfo = os.popen("adb devices").read().split("\n")
    del devicesInfo[0]
    # 删除空
    while '' in devicesInfo:
        devicesInfo.remove('')
    devicesLst = []
    devicesIdLst = []
    for i in devicesInfo:
        x = i.split("\t")
        devicesLst.append({"devicesId": x[0], "status": x[1]})
        devicesIdLst.append(x[0])
    print(devicesIdLst)
    print(devicesLst)
    return devicesIdLst, devicesLst

def subShell(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE).stdout.read().decode()



if __name__ == '__main__':
    dId, dInfo = devices()
    for phone in Config.PHONEINFO:
        if phone["devicesId"] in dId:
            pass
        else:
            print(phone, "没有devices到，请检查")

    for info in dInfo:
        if info["status"] != "device":
            print(info, "次设备不处于device状态，请检查")
        else:
            for j in Config.PHONEINFO:
                if j["devicesId"] == info["devicesId"]:
                    x = subShell(f"adb connect {j['ip']}:5555")
                    # x = os.popen(f"adb connect {j['ip']}:5555").read().decode(encoding='utf8')
                    print(x)
                    if "connected" in x:
                        print("连接成功")
                        os.popen(f"adb disconnect {j['ip']}:5555").read()
                    else:
                        os.popen(f"adb -s {info['devicesId']} tcpip 5555").read()
                        print("打开端口")
                        x = subShell(f"adb connect {j['ip']}:5555")
                        print(x)
                        if "connected" in x:
                            print("打开后连接成功")
                            os.popen(f"adb disconnect {j['ip']}:5555").read()
                        else:
                            print("无能为力，来修吧（打开端口后还是无法连接）")







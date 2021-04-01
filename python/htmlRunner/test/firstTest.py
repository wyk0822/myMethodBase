# coding=utf-8
__author__ = "wyk"

import json
import time
import webbrowser

import xlrd
config = {
    "filePath": "D_掉落组.xlsx",
    "sheetNo":1,
}
def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook(config['filePath'])
    # 获取所有sheet
    # print(workbook.sheet_names()) # [u'sheet1', u'sheet2']
    #获取sheet2
    sheet2_name= workbook.sheet_names()[config["sheetNo"]]
    # 根据sheet索引或者名称获取sheet内容
    sheet2 = workbook.sheet_by_name(sheet2_name)
    # sheet的名称，行数，列数
    # print(sheet2.name,sheet2.nrows,sheet2.ncols)
    # rows = sheet2.row_values(3) # 获取第四行内容

    cols2 = sheet2.col_values(1) # 获取第三列内容
    cols7 = sheet2.col_values(6) # 获取第三列内容
    # print (cols2)
    # print (cols7)
    #获取单元格内容的三种方法
    # print(sheet2.cell(1,0).value.encode('utf-8'))
    # print(sheet2.cell_value(1,0).encode('utf-8'))
    # print(sheet2.row(1)[0].value.encode('utf-8'))
    # # 获取单元格内容的数据类型
    # print(sheet2.cell(1,3).ctype)
    info = dict(zip(cols7, cols2))
    return info

class Template:
    DATE = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    STATUS = {
        0: 'success',
        1: 'danger'
    }
    HTML_TMPL_TOP = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>{} 挑战赛接口测试报告</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">  
        <script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
        <script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <style type="text/css">
        </style>
    </head>
    <body>
        <div class="table-responsive">
            <table class="table table-hover text-center">
                <caption>{} 挑战赛接口测试报告</caption>
                <thead>
                    <tr>
                        <th style="text-align: center;" nowrap='nowrap'>挑战赛进度编号</th>
                        <th style="text-align: center;" nowrap='nowrap'>所属比赛</th>
                        <th style="text-align: center;" nowrap='nowrap'>胜利场次</th>
                        <th style="text-align: center;" nowrap='nowrap'>失败场次</th>
                        <th style="text-align: center;" nowrap='nowrap'>必得奖励</th>
                        <th style="text-align: center;" nowrap='nowrap'>随机获得奖励</th>
                        <th style="text-align: center;" nowrap='nowrap'>实际得到奖励</th>
                        <th style="text-align: center;" nowrap='nowrap'>必得奖励是否存在</th>
                        <!-- <th style="text-align: center;" nowrap='nowrap'>实际得到的随机奖励</th> -->
                        <th style="text-align: center;" nowrap='nowrap'>是否通过</th>
                        <th style="text-align: center;" nowrap='nowrap'>详情</th>
                    </tr>
                </thead>
                <tbody>
        """.format(DATE, DATE)
    HTML_TEMP_LOOP = ""

    # 循环生成内容
    # <tr class="info">
    #     <td>110011</td>
    #     <td>1100</td>
    #     <td>1</td>
    #     <td>2</td>
    #     <td>星星*1</td>
    #     <td>礼券*10; 关前彩虹球*1; 关前双蝴蝶*1; </td>
    #     <td>星星*1</td>
    #     <td>礼券*10</td>
    #     <td>通过</td>
    #     <td><a href="">详情</a></td>
    # </tr>
    HTML_TEMP_END = """
                </tbody>


            </table>
        </div>
    </body>
    <script type="text/javascript">

    </script>
</html>
        """


class buildHtml():
    def __init__(self):
        self.html = ""
        self.temp = Template()
        self.loopHtml = ""
        self.rewardsDic = read_excel()

    def listToStr(self, lst):
        if type(lst) == type([1]):
            a = ""
            for i in lst:
                a+=str(i)
                a+=","
            return a[0: -1]
        else:
            return lst

    def rewardName(self, rewardNoLst):
        rewardNameLst = []
        for rewardNo in rewardNoLst:
            rewardNo = self.listToStr(rewardNo)
            if rewardNo in self.rewardsDic:
                rewardNameLst.append(self.rewardsDic[rewardNo])
            else:
                print("可能存在marge数据", rewardNo)
                rewardCount = rewardNo[-1]
                rewardNo = rewardNo[0:-1]+"1"
                if rewardNo in self.rewardsDic:
                    rewardNameLst.append(self.rewardsDic[rewardNo]+"*{}".format(rewardCount))

                else:
                    rewardNameLst.append("未知编号:{}".format(rewardNo))
        return rewardNameLst

    def loopTbody(self, datas):
        for data in datas:
            mustDropOutRewardsExist = []
            tf = []

            for i in data["mustDropOutRewardsExist"]:
                mustDropOutRewardsExist.append(i)
                tf.append(data["mustDropOutRewardsExist"][i])

            info = dict(zip(self.rewardName(mustDropOutRewardsExist), tf))





            serverRecvRewards = self.rewardName(data["serverRecvInfo"]["rewards"])
            mustDropOutRewards = self.rewardName(data["mustDropOutRewards"])
            mustAndMayData = self.rewardName(data["mustAndMayData"])
            mayDropOutRewards = self.rewardName(data["mayDropOutRewards"])
            # print("服务器返回数据", serverRecvRewards)
            # print("配置表必得奖励", mustDropOutRewards)
            # print("必得奖励和随机奖励", mustAndMayData)
            # print("随机奖励", mayDropOutRewards)



            if data["allStatus"] != "success" or data["mustStatus"] != "success":
                self.loopHtml += '''
                        <tr class="{}">
                            <td>{}</td>
                            <td>{}</td>
                            <td>{}</td>
                            <td>{}</td>
                            <td>{}</td>
                            <td>{}</td>
                            <td>{}</td>
                            <td>{}</td>
                            <!-- <td>礼券*10</td> -->
                            <td>失败</td>
                            <!-- <td><a href="">详情</a></td> -->
                        </tr>
                    '''.format(data["status"], data["Number"], str(data["Number"])[0:-2], data['winCount'],
                               data['loseCount'], mustDropOutRewards, mayDropOutRewards, serverRecvRewards, info)
            else:
                self.loopHtml += '''
                    <tr class="{}">
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <!-- <td>礼券*10</td> -->
                        <td>通过</td>
                        <!-- <td><a href="javascript:void(0);">详情</a></td> -->
                    </tr>
                '''.format(data["status"], data["Number"], str(data["Number"])[0:-2], data['winCount'],
                           data['loseCount'], mustDropOutRewards, mayDropOutRewards, serverRecvRewards, info)

    def build(self):
        self.html += Template.HTML_TMPL_TOP
        self.html += self.loopHtml
        self.html += Template.HTML_TEMP_END
        with open("report.html", "w", encoding='utf-8') as f:
            f.write(self.html)
        webbrowser.open("report.html")

    def run(self):
        with open("testOfEnd.json", "r", encoding='utf-8') as f:
            my_json = json.load(f)
        self.loopTbody(my_json)
        self.build()


if __name__ == '__main__':
    b = buildHtml()
    b.run()
    # b.rewardName([[1,1,3], [2,2,4]])
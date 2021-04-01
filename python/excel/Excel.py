# -*- coding: utf-8 -*-
import xlrd

class Excel:
    def __init__(self, filePath, sheetName=None, sheetNo=0):
        self.filePath = filePath
        self.sheet = sheetName
        self.sheetNo = sheetNo

    def read_excel_use_sheet_name(self):
        # 打开文件
        workbook = xlrd.open_workbook(self.filePath)
        # 获取所有sheet
        print(workbook.sheet_names()) # [u'sheet1', u'sheet2']
        #获取sheet2
        sheet2_name= workbook.sheet_names()[1]
        print(sheet2_name)
        # 根据sheet索引或者名称获取sheet内容
        sheet2 = workbook.sheet_by_name(sheet2_name)
        # sheet的名称，行数，列数
        print(sheet2.name,sheet2.nrows,sheet2.ncols)
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
        if "1,3,4700" in info:
            print(info["1,3,4700"])


if __name__ == '__main__':
    # read_excel()
    pass



"""
=========================
File: read_excel.py
Author: dancing
Time: 2019/9/28
E-mail: 1059880026@qq.com
=========================
"""
import openpyxl


class CaseData:

    def __init__(self, zip_obj, *args, **kwargs):
        for i in list(zip_obj):
            setattr(self, i[0], i[1])


# 定义一个类专门读取excel
class ReadExcel:
    """读取excel中的数据"""

    def __init__(self, file_name, sheet_name):
        """
        :param file_ name: excel文件名
        :param sheet_name: sheet表单名
        """
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.workbook = None
        self.sheet = None

    def open(self):
        # 1、打开文件，返回一个工作簿对象
        self.workbook = openpyxl.load_workbook(self.file_name)
        # 2、通过工作簿，选择表单对象
        self.sheet = self.workbook[self.sheet_name]

    def read_data(self):
        # 打开文件和表单
        self.open()
        # 按行获取所有的表格对象，每一行的内容放在一个元祖中
        rows = list(self.sheet.rows)
        # 存放所有用例
        cases = []
        # 获取表头
        title = [row.value for row in rows[0]]
        # 遍历其他内容行，并和表头打包转换成字典，存放到上面的cases中
        for row in rows[1:]:
            content = [(r.value) for r in row]
            case = dict(zip(title, content))
            cases.append(case)
        return cases

    def read_data_obj(self):
        # 打开文件和表单
        self.open()
        # 创建一个空的列表
        cases = []
        # 读取表单中的数据
        rows = list(self.sheet.rows)
        # 读取表头
        titles = [r.value for r in rows[0]]
        # print(titles)
        # 读取其他内容
        for row in rows[1:]:
            content = [r.value for r in row]
            zip_obj = zip(titles, content)
            case_data = CaseData(zip_obj)
            cases.append(case_data)
        # 将每一条用例的数据，存储为一个对象

        # 将包含所有用例的列表cases进行返回
        return cases

    def write_data(self, row, column, value):
        """
        :param row: 写入的行
        :param column: 写入的列
        :param value: 写入的内容
        """
        # 打开文件
        self.open()
        # 按照的行和列以及内容进行写入
        cell = self.sheet.cell(row, column, value=value)
        # 保存内容
        self.workbook.save(self.file_name)


if __name__ == '__main__':
    do_excel = ReadExcel('cases.xlsx', 'test_case')
    cases = do_excel.read_data_obj()
    for i in cases:
        print(i.data)

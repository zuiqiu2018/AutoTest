"""
=========================
File: test_add.py
Author: dancing
Time: 2019/10/3
E-mail: 1059880026@qq.com
=========================
"""
import os
import unittest
from package_lib.ddt import ddt, data
from common.read_excel import ReadExcel
from common.constant import DATA_DIR
from common.http_requests import HTTPSession
from common.my_logger import logger
from common.do_mysql import ReadMysql
from common.config import my_conf
from common.text_replace import data_replace


@ddt
class TestAdd(unittest.TestCase):
    """加标接口"""
    data_file_path = os.path.join(DATA_DIR, "case_data.xlsx")
    excel = ReadExcel(data_file_path, 'add')
    cases = excel.read_data_obj()
    http = HTTPSession()
    db = ReadMysql(my_conf.get('mysql', 'host'),
                   my_conf.get('mysql', 'user'),
                   my_conf.get('mysql', 'password'),
                   my_conf.getint('mysql', 'port'),
                   my_conf.get('mysql', 'database'))

    @classmethod
    def setUpClass(cls):
        logger.debug("-------开始加标接口测试{}-------")

    @classmethod
    def tearDownClass(cls):
        logger.debug("-------结束加标接口测试{}-------")

    @data(*cases)
    def test_add(self, case):
        # 第一步：入参和用例数据
        url = my_conf.get('url', 'url') + case.url + case.interface
        case.data = data_replace(case.data)
        if "*memberId*" in case.data:
            max_id = self.db.find_one("select max(id) from member")[0]
            memberId = max_id + 1
            case.data = case.data.replace("*memberId*", str(memberId))

        # 判断是否需要sql校验
        if case.check_sql:
            case.check_sql = data_replace(case.check_sql)
            # 获取当前用户加标签的数量
            start_count = self.db.find_count(case.check_sql)

        # 第二步：发送接口请求
        res = self.http.request(case.method, url, data=eval(case.data)).json()
        print(res)
        res_code = res['code']
        # 第三步：校验结果
        try:
            self.assertEqual(str(case.excepted), res_code)
            if case.check_sql:
                case.check_sql = data_replace(case.check_sql)
                # 获取当前用户加标签的数量
                end_count = self.db.find_count(case.check_sql)
                self.assertEqual(1, end_count-start_count)
        except AssertionError as e:
            # 用例执行未通过
            self.excel.write_data(case.case_id+1, 8, "fail")
            logger.info("测试数据为：{}".format(case.data))
            logger.info("期望结果是：{}".format(case.excepted_code))
            logger.info("实际结果是：{}".format(res))
            logger.exception(e)
            raise e
        else:
            self.excel.write_data(case.case_id + 1, 8, "pass")
            logger.info("测试数据为：{}".format(case.data))
            logger.info("期望结果是：{}".format(case.excepted))
            logger.info("实际结果是：{}".format(res))
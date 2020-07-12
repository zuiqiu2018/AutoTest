"""
=========================
File: test_recharge.py
Author: dancing
Time: 2019/10/2
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


@ddt
class TestRecharge(unittest.TestCase):
    """充值接口"""
    data_file_path = os.path.join(DATA_DIR, "case_data.xlsx")
    excel = ReadExcel(data_file_path, 'recharge')
    cases = excel.read_data_obj()
    http = HTTPSession()
    db = ReadMysql(my_conf.get('mysql', 'host'),
                   my_conf.get('mysql', 'user'),
                   my_conf.get('mysql', 'password'),
                   my_conf.getint('mysql', 'port'),
                   my_conf.get('mysql', 'database'))

    @data(*cases)
    def test_recharge(self, case):
        # 第一步：入参和用例数据
        url = case.url + case.interface
        # 获取充值之前的余额
        if case.check_sql:
            start_money = self.db.find_one(case.check_sql)[0]
            print("充值之前用户的余额是：{}".format(start_money))

        # 第二步：发送接口请求
        res = self.http.request(case.method, url, data=eval(case.data)).json()
        # 第三步：校验结果
        try:
            self.assertEqual(str(case.excepted_code), res["code"])
            # 获取充值之后的余额
            if case.check_sql:
                end_money = self.db.find_one(case.check_sql)[0]
                print("充值之后用户的余额是：{}".format(end_money))
                self.assertEqual(float(eval(case.data)["amount"]), float(end_money-start_money))
        except AssertionError as e:
            # 用例执行未通过
            self.excel.write_data(case.case_id+1, 10, "fail")
            logger.info("测试数据为：{}".format(case.data))
            logger.info("期望结果是：{}".format(case.excepted_code))
            logger.info("实际结果是：{}".format(res))
            logger.exception(e)
            raise e
        else:
            self.excel.write_data(case.case_id + 1, 10, "pass")
            logger.info("测试数据为：{}".format(case.data))
            logger.info("期望结果是：{}".format(case.excepted_code))
            logger.info("实际结果是：{}".format(res))
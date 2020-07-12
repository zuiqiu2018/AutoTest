"""
=========================
File: test_cases.py
Author: dancing
Time: 2019/10/1
E-mail: 1059880026@qq.com
=========================
"""
import os, random
import unittest
from package_lib.ddt import ddt, data
from common.read_excel import ReadExcel
from common.http_requests import HTTPRequest
from common.my_logger import logger
from common.constant import DATA_DIR
from common.config import my_conf
from common.do_mysql import ReadMysql
import json
from common.text_replace import data_replace


@ddt
class TestLogin(unittest.TestCase):
    file_path = os.path.join(DATA_DIR, "case_data.xlsx")
    do_excel = ReadExcel(file_path, "login")
    cases = do_excel.read_data_obj()
    db = ReadMysql(my_conf.get('mysql', 'host'),
                   my_conf.get('mysql', 'user'),
                   my_conf.get('mysql', 'password'),
                   my_conf.getint('mysql', 'port'),
                   my_conf.get('mysql', 'database'))

    # 随机生成一个手机号码
    def random_phone(self):
        phone = "13"
        # 数据库中查找该手机号是否存在
        while True:
            for i in range(9):
                num = random.randint(1, 9)
                phone += str(num)
            sql = "select * from member where MobilePhone = {};".format(
                phone)
            if not self.db.find_one(sql):
                break
        return phone

    @classmethod
    def setUpClass(cls):
        logger.debug("-------开始登录接口测试{}-------")

    @classmethod
    def tearDownClass(cls):
        logger.debug("-------结束登录接口测试{}-------")

    @data(*cases)
    def test_login(self, case):
        # 第一步：准备测试数据和入参
        excepted = case.excepted
        # url = case.url + case.interface
        url = my_conf.get('url', 'url') + case.url + case.interface
        case.data = data_replace(case.data)
        if "*phone*" in case.data:
            random_phone = self.random_phone()
            case.data = case.data.replace("*phone*", random_phone)
        request_data = eval(case.data)
        # 第二步：请求接口
        res = HTTPRequest().request(case.method, url, request_data)

        # 第三步：预期对比
        try:
            self.assertEqual(json.loads(excepted), res.json())
        except AssertionError as e:
            self.do_excel.write_data(case.case_id+1, 8, "Fail")
            logger.info("测试数据为：{}".format(request_data))
            logger.info("期望结果是：{}".format(excepted))
            logger.info("实际结果是：{}".format(res.json()))
            logger.exception(e)
            raise e
        else:
            self.do_excel.write_data(case.case_id + 1, 8, "Pass")
            logger.info("测试数据为：{}".format(request_data))
            logger.info("期望结果是：{}".format(excepted))
            logger.info("实际结果是：{}".format(res.json()))


@ddt
class TestRegister(unittest.TestCase):
    file_path = os.path.join(DATA_DIR, "case_data.xlsx")
    do_excel = ReadExcel(file_path, "register")
    cases = do_excel.read_data_obj()
    db = ReadMysql(my_conf.get('mysql', 'host'),
                   my_conf.get('mysql', 'user'),
                   my_conf.get('mysql', 'password'),
                   my_conf.getint('mysql', 'port'),
                   my_conf.get('mysql', 'database'))

    @classmethod
    def setUpClass(cls):
        logger.debug("-------开始注册接口测试{}-------")

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        logger.debug("-------结束注册接口测试{}-------")

    @data(*cases)
    def test_register(self, case):
        # 第一步：准备测试数据和入参
        excepted = case.excepted
        url =my_conf.get('url', 'url') + case.url + case.interface
        # 替换动态化参数
        random_phone = self.random_phone()
        case.data = case.data.replace("*phone*", random_phone)
        request_data = eval(case.data)

        # 第二步：发送接口请求
        res = HTTPRequest().request(case.method, url, request_data)

        # 第三步：比对结果
        try:
            self.assertEqual(json.loads(excepted), res.json())
            try:
                if case.check_sql:
                    logger.debug("此条用例走了if语句")
                    count = self.db.find_count(case.check_sql.replace("*phone*", random_phone))
                    self.assertEqual(1, count)
                    logger.info("测试数据为：1")
                    logger.info("期望结果是：{}".format(count))
                else:
                    logger.debug("此条用例没有走if语句")
            except AssertionError as e:
                logger.exception(e)
                raise e
        except AssertionError as e:
            self.do_excel.write_data(case.case_id+1, 8, "Fail")
            logger.info("测试数据为：{}".format(request_data))
            logger.info("期望结果是：{}".format(excepted))
            logger.info("实际结果是：{}".format(res.json()))
            logger.exception(e)
            raise e
        else:
            self.do_excel.write_data(case.case_id + 1, 8, "Pass")
            logger.info("测试数据为：{}".format(request_data))
            logger.info("期望结果是：{}".format(excepted))
            logger.info("实际结果是：{}".format(res.json()))

    # 随机生成一个手机号码
    def random_phone(self):
        phone = "13"
        # 数据库中查找该手机号是否存在
        while True:
            for i in range(9):
                num = random.randint(1, 9)
                phone += str(num)
            sql = "select * from member where MobilePhone = {};".format(
                phone)
            if not self.db.find_one(sql):
                break
        return phone


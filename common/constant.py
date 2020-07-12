"""
=========================
File: constant.py
Author: dancing
Time: 2019/9/30
E-mail: 1059880026@qq.com
=========================
"""
import os
"""
常量模块，获取项目目录的路径，保存

项目路径
用例类所在路径：
配置文件的路径：
用例数据的路径：
日志文件的路径：
测试报告的路径：
"""

print(__file__)

# 项目目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 用例类所在路径
CASES_DIR = os.path.join(BASE_DIR, 'test_cases')

# 配置文件的路径
CONF_DIR = os.path.join(BASE_DIR, 'conf')

# 用例数据的路径
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 日志文件的路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 测试报告的路径
REPORT_DIR = os.path.join(BASE_DIR, 'report')


if __name__ == '__main__':
    print(BASE_DIR)
    print(CASES_DIR)
    print(CONF_DIR)
    print(DATA_DIR)
    print(LOG_DIR)
    print(REPORT_DIR)

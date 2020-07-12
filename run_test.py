"""
=========================
File: run_test.py
Author: dancing
Time: 2019/10/1
E-mail: 1059880026@qq.com
=========================
"""
import os, time
import unittest
from HTMLTestRunnerNew import HTMLTestRunner
from common.constant import REPORT_DIR
from test_cases import test_cases

# 第一步：创建测试套件
suite = unittest.TestSuite()

# 第二步：加载测试用例
loader = unittest.TestLoader()
# suite.addTest(loader.discover(CASES_DIR))
suite.addTest(loader.loadTestsFromModule(test_cases))

# 第三步：执行并生成报告
now = time.strftime("%Y-%m-%d_%H_%M_%S")
report_path = os.path.join(REPORT_DIR, now + 'report.html')

with open(report_path, 'wb') as f:
    runner = HTMLTestRunner(stream=f,
                            verbosity=2,
                            title="frame_design",
                            description="practice_test",
                            tester="dancing")
    runner.run(suite)

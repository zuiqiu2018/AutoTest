"""
=========================
File: my_logger.py
Author: dancing
Time: 2019/9/29
E-mail: 1059880026@qq.com
=========================
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from common.config import my_conf


log_level = my_conf.get("log", "log_level")
f_level = my_conf.get("log", "f_level")
s_level = my_conf.get("log", "s_level")
filename = my_conf.get("log", "log.log")


class MyLogging(object):

    # 创建对象的
    def __new__(cls, *args, **kwargs):
        logger = logging.getLogger('my_logging')
        # 设置日志收集器收集的日志等级
        logger.setLevel(log_level)

        # 创建一个按时间轮转的输出渠道
        fh = TimedRotatingFileHandler(filename, encoding="utf8", when='D',
                                      backupCount=7)
        fh.setLevel(f_level)
        sh = logging.StreamHandler()
        sh.setLevel(s_level)

        # 将收集渠道添加到收集器中
        logger.addHandler(fh)
        logger.addHandler(sh)

        # 设置日志输出格式
        formatter = logging.Formatter(
            "%(asctime)s-【%(filename)s-->line%(lineno)d】-%(levelname)s-%(message)s")

        # 把输出格式绑定到输出渠道上
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)
        return logger


logger = MyLogging()


"""
=========================
File: config.py
Author: dancing
Time: 2019/9/29
E-mail: 1059880026@qq.com
=========================
"""
import os
from configparser import ConfigParser

from common.constant import CONF_DIR


class MyConfig(ConfigParser):

    def __init__(self):
        super().__init__()
        c = ConfigParser()
        c.read(os.path.join(CONF_DIR, 'env.ini'), encoding="utf8")

        env = c.get('env', 'switch')
        print(env)
        # 根据开关的值去读取不同的环境
        if env == 1:
            self.read(os.path.join(CONF_DIR, "conf.ini"), encoding="utf8")
        elif env == 2:
            self.read(os.path.join(CONF_DIR, "conf1.ini"), encoding="utf8")

        # 初始化的时候，打开配置文件
        else:
            self.read(os.path.join(CONF_DIR, "conf.ini"), encoding="utf8")


def my_config():
    conf = ConfigParser()
    conf.read(os.path.join(CONF_DIR, "conf.ini"))
    return conf


# my_conf = my_config()
my_conf = MyConfig()

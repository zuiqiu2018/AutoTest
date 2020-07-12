"""
=========================
File: text_replace.py
Author: dancing
Time: 2019/10/3
E-mail: 1059880026@qq.com
=========================
"""
import re
from common.config import my_conf


"""
封装一个替换数据的方法

封装的需求：
1、替换用例中的参数
2、简化替换的流程

实现思路：
1、获取用例数据
2、判断该条用例数据是否有需要替换的数据
3、对数据进行替换
"""


class ConText:
    """通过setattr()的方式，来临时保存接口之间依赖参数的类，
    比把数据固定在配置文件中要好，因为配置文件写死了"""
    pass


def data_replace(data):
    while re.search(r"#(.+?)#", data):
        res = re.search(r"#(.+?)#", data)
        # 获取匹配的内容
        r_data = res.group()
        # 提取要替换的内容
        key = res.group(1)
        # 通过提取的字段，去配置文件中读取对应的数据内容
        try:
            value = my_conf.get('data', key)
        except:
            value = getattr(ConText, key)
        data = re.sub(r_data, value, data)
    return data



if __name__ == '__main__':
    data = '{"mobilephone":"#phone#","pwd":"#pwd#","regname":"123"}'
    print(data_replace(data))





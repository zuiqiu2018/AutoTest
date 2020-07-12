"""
=========================
File: do_mysql.py
Author: dancing
Time: 2019/10/1
E-mail: 1059880026@qq.com
=========================
"""
import pymysql
from common.config import my_conf


class ReadMysql:

    def __init__(self, host, user, password, port, database):
        self.conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                database=database,
                charset='utf8')
        self.cur = self.conn.cursor()

    def close(self):
        # 关闭游标
        self.cur.close()
        # 断开连接
        self.conn.close()

    def find_one(self, sql):
        """查询一条数据"""
        self.conn.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_all(self,sql):
        """查询多条数据"""
        self.conn.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_count(self,sql):
        """查询数据的条数"""
        self.conn.commit()
        count = self.cur.execute(sql)
        return count


if __name__ == '__main__':
    # sql0 = "select * from member where MobilePhone = '18330372028';"
    # sql_test = "select * from member where MobilePhone = '18624443456';"
    # sql1 = "select * from member limit 5;"
    host = my_conf.get("mysql", "host")
    port = my_conf.getint("mysql", "port")
    user = my_conf.get("mysql", "user")
    password = my_conf.get("mysql", "password")
    database = my_conf.get("mysql", "database")

    db = ReadMysql(host, user, password, port, database)
    # res = db.find_all(sql0)
    # print(res)
    # res1 = db.find_count(sql_test)
    # print(res1)

    # 数据库中查找该手机号是否存在
    # import random
    # while True:
    #     phone = "13"
    #     for i in range(9):
    #         num = random.randint(1, 9)
    #         phone += str(num)
    #     print(phone)
    #     sql = "select * from member where MobilePhone = {};".format(
    #         phone)
    #     if db.find_one(sql):
    #         break
    # print(phone)
    import random

    phone = "13"
    for i in range(9):
        num = random.randint(1, 9)
        phone += str(num)
    print(phone)
    sql = "select * from member where MobilePhone = '13572283756';".format(phone)
    if db.find_one(sql):
        print(db.find_one(sql))
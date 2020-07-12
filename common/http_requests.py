"""
=========================
File: http_requests.py
Author: dancing
Time: 2019/9/30
E-mail: 1059880026@qq.com
=========================
"""
import requests


class HTTPRequest(object):
    """直接发请求不记录cookies信息"""

    @staticmethod
    def request(method, url, data=None, headers=None):
        method = method.lower()
        if method == "post":
            return requests.post(url=url, data=data, headers=headers)
        elif method == "get":
            return requests.get(url=url, params=data, headers=headers)


class HTTPSession(object):
    """使用session对象发送请求，自动记录cookies信息"""

    def __init__(self):
        # 创建一个session对象
        self.session = requests.session()

    def request(self, method, url, data=None, headers=None):
        method = method.lower()
        if method == "post":
            return self.session.post(url=url, data=data, headers=headers)
        elif method == "get":
            return self.session.get(url=url, params=data, headers=headers)

    def close(self):
        self.session.close()


if __name__ == '__main__':
    data1 = {"mobilephone":"13572283756","pwd": "abcdefg"}
    http = HTTPSession()
    res = http.request('POST',
                       'http://test.lemonban.com/futureloan/mvc/api/member/login',
                       data=data1)
    print(res.json())
    # data2 = {"memberId":170618,
    #          "title": "i need money",
    #          "amount":10000.00,
    #          "loanRate": 18.0,
    #          "loanTerm": 6,
    #          "loanDateType": 0,
    #          "repaymemtWay": 4,
    #          "biddingDays":10}
    data2 = {"memberId": 170618, "title": "i need money", "amount": 10000.00,
     "loanRate": 18.0, "loanTerm": 6, "loanDateType": 0, "repaymemtWay": 4,
     "biddingDays": 10}
    res = http.request('POST',
                       'http://test.lemonban.com/futureloan/mvc/api/loan/add',
                       data=data2)
    print(res.json())
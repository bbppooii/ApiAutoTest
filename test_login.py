'''
登录——接口自动化测试
url:http://8.137.19.140:9090/user/login  POST
form-data {"username":"zhangsan","password":"123456"}
'''
import re

import pytest

from jsonschema import validate
from utils.request_util import host, Request
from utils.yaml_util import write_yaml

@pytest.mark.order(1)
class TestLogin:
    url = host + "user/login"
    schema = {
      "type": "object",
      "required": ["code","errMsg","data"],
      "additionalProperties": False,
      "properties": {
        "code": {
          "type": "string"
        },
        "errMsg": {
          "type": "string"
        },
        "data": {
          "type": ["string","null"]
        }
      }
    }

    @pytest.mark.parametrize("login",[
        #错误的账号和密码
        {
            "username": "zhang",
            "password": "123",
            "errMsg":"用户不存在"
        },
        #错误的账号，正确的密码
        {
            "username": "zhang",
            "password": "123456",
            "errMsg": "用户不存在"
        },
        #正确的账号，错误的密码
        {
            "username": "zhangsan",
            "password": "123",
            "errMsg":"密码错误"
        },
        #不存在的账号
        {
            "username": "bitetest",
            "password": "xxxxxx",
            "errMsg": "用户不存在"
        },
        #账号和密码都为空
        {
            "username": "",
            "password": "",
            "errMsg": "账号或密码不能为空"
        },
        #过长的账号
        {
            "username": "这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号",
            "password": "123456",
            "errMsg": "用户不存在"
        },
        #过长的密码
        {
            "username": "zhangsan",
            "password": "这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码",
            "errMsg": "密码错误"
        }
    ])
    #异常登录——放在正常登录之前 ？
    def test_login_fail(self,login):
        data = {
            "username": login["username"],
            "password": login["password"]
        }
        r = Request().post(url=self.url, data=data)

        validate(instance=r.json(), schema=self.schema)

        assert r.json()["code"] == "FAIL"
        assert r.json()['errMsg'] == login["errMsg"]


    #正常登录
    @pytest.mark.parametrize("login",[
        {
            "username":"zhangsan",
            "password":"123456",
        },
        {
            "username": "lisi",
            "password": "123456",
        }
    ])
    def test_login_success(self,login):
        data = {
            "username": login["username"],
            "password": login["password"]
        }
        r = Request().post(url=self.url,data=data)

        validate(instance=r.json(),schema=self.schema)

        assert r.json()["code"] == "SUCCESS"
        assert re.match('\S{100,}',r.json()['data'])

        #接口返回的data就是用户的登录凭证----作为其他接口的登录凭证

        token = {
            "user_token_header":r.json()['data']
        }
        write_yaml("data.yml",token)
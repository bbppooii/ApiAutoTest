'''
添加博客接口
'''
from pickle import FALSE

import pytest
from jsonschema import validate

from utils.request_util import host, Request
from utils.yaml_util import read_yaml


class TestAdd:
    url = host + "blog/add"
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
          "type": "boolean"
        }
      }
    }

    #未登录状态下请求add接口
    def test_add_noLogin(self):
        r = Request().post(url=self.url)
        r.status_code == 401

    #测试添加博客——添加成功+添加失败
    @pytest.mark.parametrize("add",[
        #添加成功
        {
            "title": "接口自动化标题",
            "content": "接口自动化内容",
            "data":True
        },
        #标题为空
        {
            "title": "",
            "content": "接口自动化内容",
            "data": False
        },
        #内容为空
        {
            "title": "接口自动化标题",
            "content": "",
            "data": False
        },
        #标题和内容都为空
        {
            "title": "",
            "content": "",
            "data": False
        },
        #添加带有图片的博客
        {
            "title": "接口自动化标题--带有图片",
            "content": "![](https://pic.rmb.bdstatic.com/bjh/down/gxGspORnpcqm_GBISeO0iQ15d06ce241eb6b8aa7da1dcf17317911.jpg?for=bg)",
            "data": True
        },
        #添加带有链接的博客
        {
            "title": "接口自动化标题--带有链接",
            "content": "[百度首页](http://www.baidu.com \"百度首页\")",
            "data": True
        },
    ])
    def test_add(self,add):

        token = read_yaml("data.yml","user_token_header")
        header = {
            "user_token_header":token
        }

        json = {
            "title": add["title"],
            "content": add["content"]
        }

        r = Request().post(url=self.url,json = json,headers = header)
        #验证jsonSchema
        validate(instance=r.json(),schema=self.schema)

        #assert关键字段的值要匹配
        assert r.json()['data'] == add["data"]
import pytest

from jsonschema import validate
from urllib3.util.util import to_str
from utils.request_util import host, Request
from utils.yaml_util import read_yaml


class TestDetail:
    url = host +"blog/getBlogDetail"
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
          "type": "object",
          "additionalProperties": False,
          "required": ["id","title","content","userId","deleteFlag","createTime","updateTime","loginUser"],
          "properties": {
            "id": {
              "type": "number"
            },
            "title": {
              "type": "string"
            },
            "content": {
              "type": "string"
            },
            "userId": {
              "type": "number"
            },
            "deleteFlag": {
              "type": "number"
            },
            "createTime": {
              "type": "string"
            },
            "updateTime": {
              "type": "string"
            },
            "loginUser": {
              "type": "boolean"
            }
          }
        }
      }
    }

    #未登录状态下访问博客详情页
    def test_detail_noLogin(self):
        url = self.url + "?blogId=1234"
        r = Request().get(url=url)
        assert r.status_code == 401

    #登录状态下请求博客详情页
    #正常请求
    def test_detail_login(self):
        url = self.url + "?blogId=" + str(read_yaml("data.yml","blogId"))
        token = read_yaml("data.yml", "user_token_header")
        header = {
            "user_token_header": token
        }
        r = Request().get(url=url,headers=header)

        #jsonSchema校验
        validate(instance=r.json(),schema=self.schema)
        #assert关键字段值的校验
        assert r.json()["code"] == "SUCCESS"

    #博客详情页——blogId错误
    @pytest.mark.parametrize("blogId",["",1234,"比特",-100,999999999999999999999999999999999999])
    def test_detail_fail(self,blogId):
        url = self.url
        #配置参数
        params = {
            "blogId":blogId
        }

        token = read_yaml("data.yml", "user_token_header")
        header = {
            "user_token_header": token
        }
        r = Request().get(url=url, headers=header)

        expect_json = {
            "code": "FAIL",
            "errMsg": "内部错误, 请联系管理员",
            "data": None
        }

        assert r.json() == expect_json



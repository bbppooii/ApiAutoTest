import pytest
from jsonschema import validate
from utils.request_util import host, Request
from utils.yaml_util import read_yaml


class TestgetAuthorInfo:
    url = host + "user/getAuthorInfo"
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
          "type": ["object","null"],
          "additionalProperties": False,
          "required": ["id","userName","password","githubUrl","deleteFlag","createTime","updateTime"],
          "properties": {
            "id": {
              "type": "number"
            },
            "userName": {
              "type": "string"
            },
            "password": {
              "type": "string"
            },
            "githubUrl": {
              "type": "string"
            },
            "deleteFlag": {
              "type": "number"
            },
            "createTime": {
              "type": "string"
            },
            "updateTime": {
              "type": "string"
            }
          }
        }
      }
    }

    #未登录状态访问接口
    def test_getAuthorInfo_noLogin(self):
        url = self.url + "?blogId=24314"
        r = Request().get(url=url)
        assert r.status_code == 401

    #登录状态下正确请求
    #有效的blogId
    def test_getAuthorInfo(self):
        blogId = read_yaml("data.yml","blogId")
        url = self.url + "?blogId=" + str(blogId)
        #读取用户登录凭证
        token = read_yaml("data.yml","user_token_header")
        header = {
            "user_token_header" : token
        }
        #发起请求
        r = Request().get(url = url,headers = header)

        #校验jsonschema
        validate(instance=r.json(),schema=self.schema)
        #asser校验关键数据
        assert r.json()['code'] == "SUCCESS"

    #登录状态下异常请求
    #blogId异常
    @pytest.mark.parametrize("blogId,expected_code",[
        ("","FAIL"),
        (1234,"FAIL"),
        (-100,"SUCCESS"),
        ("比特","FAIL"),
        (999999999999999999999999999999999999,"FAIL")
    ])
    def test_getAuthorInfo_fail(self,blogId,expected_code):
        url = self.url
        # 配置参数
        params = {
            "blogId": blogId
        }
        # 读取用户登录凭证
        token = read_yaml("data.yml", "user_token_header")
        header = {
            "user_token_header": token
        }
        # 发起请求
        r = Request().get(url=url, headers=header,params = params)

        validate(instance=r.json(),schema=self.schema)
        assert r.json()["code"] == expected_code



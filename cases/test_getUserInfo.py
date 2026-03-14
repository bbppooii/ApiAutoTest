from jsonschema import validate
from utils.request_util import host, Request
from utils.yaml_util import read_yaml


class TestgetUserInfo:
    url = host + "user/getUserInfo"
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

    #未登陆状态下请求接口
    def test_getUserInfo_noLogin(self):
        r = Request().get(url=self.url)
        assert r.status_code  == 401

    #登陆状态下请求接口
    def test_getUserInfo(self):
        #添加请求头
        token = read_yaml("data.yml","user_token_header")
        header = {
            "user_token_header":token
        }
        r = Request().get(url=self.url,headers = header)
        #校验jsonschema
        validate(instance=r.json(),schema=self.schema)
        #assser校验关键数据
        assert r.json()["code"] == "SUCCESS"


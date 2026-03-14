import pytest
from jsonschema import validate
from utils.request_util import host, Request
from utils.yaml_util import read_yaml, write_yaml

@pytest.mark.order(2)
class TestList:
    url = host + "blog/getList"
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
          "type": "array",
          #要求返回的博客数据最少要有一个
          "minItems": 1,
          "items": {
            "type": "object",
            "required": ["id","title","content","userId","deleteFlag","createTime","updateTime","loginUser"],
            "additionalProperties": False,
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
    }

    #未登录的状态下请求列表页--401
    def test_list_noLogin(self):
        r = Request().get(url=self.url)
        assert r.status_code == 401

    #请求列表页——登录的场景下
    def test_list_login(self):
        token = read_yaml("data.yml","user_token_header")
        header = {
            "user_token_header":token
        }
        r = Request().get(url=self.url,headers = header)
        #jsonSchema校验
        validate(instance=r.json(),schema=self.schema)
        #关键字段值的校验
        assert r.json()['code'] == "SUCCESS"

        #提取有效的blogid存储在yaml文件中
        blogId = {
            "blogId":r.json()['data'][0]["id"]
        }
        write_yaml("data.yml",blogId)

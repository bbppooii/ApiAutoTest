import requests
from utils.logger_util import logger

host = "http://8.137.19.140:9090/"

class Request:
    log  = logger.getlog()

    def get(self,url,**kwargs):
        self.log.info("准备发起get请求，url:"+url)
        self.log.info("接口信息：{}".format(kwargs))

        r = requests.get(url=url,**kwargs)

        self.log.info("接口响应状态码：{}".format(r.status_code))
        self.log.info("接口响应内容：{}".format(r.text))

        return r

    def post(self,url,**kwargs):
        self.log.info("准备发起post请求，url:"+url)
        self.log.info("接口信息：{}".format(kwargs))

        r = requests.post(url=url,**kwargs)

        self.log.info("接口响应状态码：{}".format(r.status_code))
        self.log.info("接口响应内容：{}".format(r.text))

        return r
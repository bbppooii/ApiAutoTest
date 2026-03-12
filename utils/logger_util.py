import logging
import os.path
import time

class infoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

class errFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


class logger:

    #获取日志对象---定义类方法@classmethod
    @classmethod
    def getlog(cls):

        #创建日志对象
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)

        #保证logs文件夹必须创建好了
        LOG_PATH = "./logs/"
        if not os.path.exists(LOG_PATH):
            os.mkdir(LOG_PATH)

        #将日志输出到日志文件中
        '''
        logs
            2025-12-12.log
            2025-12-12-info.log
            2025-12-12-err.log
        '''
        now = time.strftime("%Y-%m-%d")
        log_name = LOG_PATH + now + ".log"
        info_log_name = LOG_PATH + now + "-info.log"
        err_log_name = LOG_PATH + now + "-err.log"


        #创建文件处理器
        all_handler = logging.FileHandler(log_name,encoding="utf-8")
        info_handler = logging.FileHandler(info_log_name,encoding="utf-8")
        err_handler = logging.FileHandler(err_log_name,encoding="utf-8")

        #创建处理器，将日志输出到控制台
        streamHandler = logging.StreamHandler()


        #设置日志的格式
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d)] - %(message)s"
        )

        all_handler.setFormatter(formatter)
        info_handler.setFormatter(formatter)
        err_handler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        #添加过滤器
        info_handler.addFilter(infoFilter())
        err_handler.addFilter(errFilter())

        cls.logger.addHandler(all_handler)
        cls.logger.addHandler(info_handler)
        cls.logger.addHandler(err_handler)
        # cls.logger.addHandler(streamHandler)

        return cls.logger


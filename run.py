from utils.logger_util import logger

if __name__ == "__main__":
    log = logger.getlog()
    log.info("---info message---")
    log.error("---error message--")
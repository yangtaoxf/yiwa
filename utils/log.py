# coding: utf8

"""日志处理"""

import os
import logging

BASE_DIR = os.getcwd()


def path_join(*paths, filename=None, overwrite=False):
    """拼接文件/文件夹完整路径，若文件/文件夹不存在则创建
        :overwrite: 覆盖替换文件
    """
    path = os.path.join(BASE_DIR, *paths)
    if not os.path.exists(path):
        os.makedirs(path)

    if filename:
        path = os.path.join(path, filename)

    if overwrite and os.path.isfile(path):
        if os.path.exists(path):
            os.remove(path)
    return path


class Log(object):
    """"""

    def __init__(self, filename=None):
        super(Log, self).__init__()
        self._web_log = filename if filename else "web.log"
        self._yiwa_log = filename if filename else "yiwa.log"
        self._log_template = '[%(asctime)s] %(levelname)s ' + \
                             '[%(funcName)s: %(filename)s, %(lineno)d] %(message)s'

    def _log_path(self, filename):
        return path_join(BASE_DIR, "logs", filename=filename)

    @property
    def handler(self):
        """参考https://www.polarxiong.com/archives/Flask使用日志记录到文件示例.html"""

        handler = logging.FileHandler(self._log_path(self._web_log), encoding="UTF-8")
        handler.setLevel(logging.INFO)
        logging_format = logging.Formatter(self._log_template)
        handler.setFormatter(logging_format)
        return handler

    @property
    def logger(self):
        logging.basicConfig(
            level=logging.DEBUG,
            filename=self._log_path(self._yiwa_log),
            format=self._log_template,
            datefmt='%Y-%m-%d %H:%M:%S',
            filemode='a'
        )
        # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
        _console = logging.StreamHandler()
        _console.setLevel(logging.INFO)
        _formatter = logging.Formatter(self._log_template)
        _console.setFormatter(_formatter)
        logging.getLogger(self._yiwa_log).addHandler(_formatter)
        return logging


if __name__ == "__main__":
    logger = Log("test.log").logger
    logger.info("test")
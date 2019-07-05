# coding: utf8

"""yiwa后台-语音、浏览器、数据库等处理"""

from asr.stt import listening, wakeup
from asr.awake import read_keywords
from nlp.comparison import match
from importlib import import_module
from yiwa.settings import HOST, PORT
import time
from yiwa.db import DataConveyor
from yiwa.browser import create as create_browser
from yiwa.log import Log
from jieba import lcut, lcut_for_search

logger = Log().logger

ROOT = f"http://{HOST}:{PORT}"

if __name__ == "__main__":
    WAKEUP = False
    FAILURE = 0
    data_conveyor = DataConveyor()
    data_conveyor._init()
    keywords = read_keywords()
    browser = create_browser()
    browser.get(ROOT)


    def _todo(browser, action: str):
        """做action对应的动作"""
        mothed_path = action.split(".")
        package_path = ".".join(mothed_path[:-1])
        mothed_name = mothed_path[-1]
        if package_path and mothed_name:
            try:
                package = import_module(package_path)
                todo = package.__getattribute__(mothed_name)
                todo(browser)
            except Exception as e:
                logger.error(f"动态执行页面动作失败：{e}")


    def _command_filter(command):
        """过滤指令，缩小遍历范围"""
        # 相同指令
        same_commands = data_conveyor.filter_command(command)
        if same_commands:
            return same_commands

        # 分词匹配指令，有限的硬件资源环境不允许本地NLP
        all_commands = data_conveyor.all_command()

        def __filter_by_words(_words):
            actions = []
            for commands, action in all_commands:
                for _word in _words:
                    if _word in commands:
                        actions.append(action)
            return data_conveyor.filter_command_by_actions(set(actions))

        # 像似分词 https://cuiqingcai.com/5844.html
        cut_words = lcut_for_search(command)
        like_commands = __filter_by_words(cut_words)
        if like_commands:
            return like_commands

        # 模糊分词
        cut_all_words = lcut(command, cut_all=True)
        vague_commands = __filter_by_words(cut_all_words)
        if vague_commands:
            return vague_commands

        # 无匹配
        return []


    def _exec():
        """执行指令"""
        access = False  # 成功执行指令
        voice2text = listening()
        logger.info(f"发出指令>>> {voice2text}")
        data_conveyor.stt(voice2text)
        if voice2text is None:
            return access

        print(_command_filter(voice2text))

        for commands, action in _command_filter(voice2text):
            found = False  # 指令是否已找到
            for command in commands.split(","):
                if match(voice2text, command):
                    logger.info(f"指令命中: {command}")
                    data_conveyor.access(command)  # 指令入库
                    if action.startswith("/"):
                        # 页面访问
                        browser.get(ROOT + action)
                    else:
                        # 页面动作
                        _todo(browser, action)
                    data_conveyor.hot(action)  # +指令热度
                    found = True
                    break
            if found:
                access = True
                break
        else:
            logger.info("~_~ 指令不匹配")
            data_conveyor.info("~_~ 指令不匹配")
        return access


    while True:
        try:
            if WAKEUP:
                FAILURE = 0 if _exec() else (FAILURE + 1)
            else:
                word, up = wakeup(keywords)
                data_conveyor.stt(word)
                if up:
                    WAKEUP = True
                    logger.info("^_^ 唤醒成功")
                    data_conveyor.wakeup()
                    FAILURE = 0 if _exec() else (FAILURE + 1)
                else:
                    data_conveyor.stt("")
            # 10次超时， 睡眠
            if FAILURE >= 10:
                logger.info("--! 睡眠待命")
                data_conveyor.sleep()
                WAKEUP = False
                FAILURE = 0
        except Exception as e:
            logger.error(f"接收语音错误，{e}")
            data_conveyor.error()

        time.sleep(1)
    browser.close()

# coding: utf8

"""yiwa后台-语音、浏览器、数据库等处理"""

from asr.stt import listening, wakeup
from asr.awake import read_keywords
from nlp.comparison import match
from importlib import import_module
from web import HOST, PORT
import time
from utils.db import select, execute
from utils.browser import create as create_browser
from utils.log import Log

logger = Log().logger

ROOT = f"http://{HOST}:{PORT}"


class DataConveyor(object):
    """yiwa数据交互类"""

    def __init__(self):
        super(DataConveyor, self).__init__()
        self.init_captions = {
            0: "请对着我，喊我的名字吧：",
            1: "请对着我，说出指令吧：",
            -1: "很抱歉，我出错了，请重启机器吧。",
        }

    def get_commands(self):
        sql = "SELECT commands, action FROM commands ORDER BY hot DESC"
        return select(sql)

    def _init(self):
        sql = "SELECT id FROM yiwa"
        if select(sql):
            self.sleep()
        else:
            sql_init_insert = f"""INSERT INTO yiwa(status, caption, stt) 
                VALUES(0, "{self.init_captions.get(0)}", "暂无指令")
                """
            execute(sql_init_insert)

    def sleep(self):
        sql = f"""UPDATE yiwa SET status = 0,
            caption="{self.init_captions.get(0)}",
            stt="暂无指令"
            """
        execute(sql)

    def wakeup(self):
        sql = f"""UPDATE yiwa SET status = 1,
            caption="{self.init_captions.get(1)}"
            """
        execute(sql)

    def error(self):
        sql = f"""UPDATE yiwa SET status = -1,
            caption="{self.init_captions.get(-1)}"
            """
        execute(sql)

    def stt(self, command):
        sql = f"""UPDATE yiwa SET stt="{command}"
        """
        execute(sql)

    def hot(self, action):
        """增加动作的热度"""
        sql = f"""UPDATE commands SET hot=hot+1 
            WHERE action="{action}"
            """
        execute(sql)


if __name__ == "__main__":
    WAKEUP = False
    FAILURE = 0
    data_conveyor = DataConveyor()
    data_conveyor._init()
    keywords = read_keywords()
    browser = create_browser()


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


    def _exec():
        """执行指令"""
        access = False  # 成功执行指令
        voice2text = listening()
        logger.info(f"指令>>> {voice2text}")
        print(f"指令>>> {voice2text}")
        if voice2text is None:
            logger.info("空指令")
            data_conveyor.stt("指令无效")
            return access

        for commands, action in data_conveyor.get_commands():
            found = False  # 指令是否已找到
            for command in commands.split(","):
                if match(voice2text, command):
                    data_conveyor.stt(command)  # 指令入库
                    if action.startswith("/"):
                        # 页面访问
                        browser.get(ROOT + action)
                    else:
                        # 页面动作
                        _todo(browser, action)
                    data_conveyor.hot(action)   # +指令热度
                    found = True
                    break
            if found:
                access = True
                break
        else:
            logger.info("指令不匹配")
        return access


    while True:
        try:
            if WAKEUP:
                FAILURE = 0 if _exec() else (FAILURE + 1)
            else:
                word, up = wakeup(keywords)
                if up:
                    logger.info("唤醒成功")
                    WAKEUP = True
                    FAILURE = 0 if _exec() else (FAILURE + 1)
                    data_conveyor.wakeup()
                    data_conveyor.stt(word)
                else:
                    data_conveyor.stt("指令无效")
            # 10次超时， 睡眠
            if FAILURE >= 10:
                logger.info("睡眠待命")
                WAKEUP = False
                FAILURE = 0
                data_conveyor.sleep()
        except:
            data_conveyor.error()

        time.sleep(1)
    browser.close()

# coding: utf8

"""数据库操作，未使用装饰器（数据操作对象传递是个麻烦问题）
或者类处理（目前不是频繁使用，类的得不到及时注销将会常驻内存）"""

import os
import sqlite3
from yiwa.settings import BASE_DIR

DB_FILE = os.path.join(BASE_DIR, "yiwa.s3db")

def select(sql):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
        return result


def execute(sql):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

def executemany(sql, data):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.executemany(sql, data)
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


class DataConveyor(object):
    """yiwa数据交互类"""

    def __init__(self):
        super(DataConveyor, self).__init__()
        self.init_captions = {
            0: "请对着我，喊我的名字吧：",
            1: "请对着我，说出指令吧：",
            -1: "很抱歉，我出错了，请重启机器吧。",
        }


    def _init(self):
        sql = "SELECT id FROM yiwa"
        if select(sql):
            self.sleep()
        else:
            sql_init_insert = f"""INSERT INTO yiwa(status, caption, listening, info, stt) 
                VALUES(0, "{self.init_captions.get(0)}", 0, "等待唤醒", "")
                """
            execute(sql_init_insert)

    def sleep(self):
        sql = f"""UPDATE yiwa SET status = 0,
            caption="{self.init_captions.get(0)}",
            listening=0,
            info="--! 睡眠待命",
            stt=""
            """
        execute(sql)

    def wakeup(self):
        sql = f"""UPDATE yiwa SET status = 1,
            caption="{self.init_captions.get(1)}",
            info="^_^ 唤醒成功"
            """
        execute(sql)

    def access(self, command):
        sql = f"""UPDATE yiwa SET status = 1,
            caption="{self.init_captions.get(1)}",
            info="指令命中: {command}"
            """
        execute(sql)

    def error(self):
        sql = f"""UPDATE yiwa SET status = -1,
            caption="{self.init_captions.get(-1)}",
            info="接收语音发送错误"
            """
        execute(sql)

    def stt(self, command):
        if not command:
            command = "-"
        sql = f"""UPDATE yiwa SET stt="{command}"
        """
        execute(sql)

    def info(self, info):
        if not info:
            info = "-"
        sql = f"""UPDATE yiwa SET info="{info}"
        """
        execute(sql)

    def listening(self):
        """监听中"""
        sql = f"""UPDATE yiwa SET listening = 1,
            info="录音中"
            """
        execute(sql)

    def listened(self):
        """监听完毕"""
        sql = f"""UPDATE yiwa SET listening = 0,
            info="录音结束"
            """
        execute(sql)

    def all_command(self):
        sql = "SELECT commands, action FROM commands ORDER BY hot DESC"
        return select(sql)

    def filter_command(self, command):
        sql = f"""SELECT commands, action FROM commands 
          WHERE commands LIKE "%{command}%" 
          ORDER BY hot DESC"""
        return select(sql)

    def filter_command_by_actions(self, actions):
        if not actions:
            return []
        in_actions = "','".join(actions)
        sql = f"""SELECT commands, action FROM commands 
          WHERE action IN ('{in_actions}') 
          ORDER BY hot DESC"""
        return select(sql)

    def hot(self, action):
        """增加动作的热度"""
        sql = f"""UPDATE commands SET hot=hot+1 
            WHERE action="{action}"
            """
        execute(sql)
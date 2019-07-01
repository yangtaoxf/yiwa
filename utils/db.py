# coding: utf8

"""数据库操作，未使用装饰器（数据操作对象传递是个麻烦问题）
或者类处理（目前不是频繁使用，类的得不到及时注销将会常驻内存）"""

import sqlite3

DB_FILE = "yiwa.s3db"

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
# coding: utf8

"""yiwa-WEB后端"""

from __future__ import absolute_import
from apps import app, socketio
from yiwa.io import scan_apps
from yiwa.db import execute, executemany
import subprocess
from yiwa.log import Log
from flask import redirect, render_template
from tdcode import qr_code
from yiwa.settings import HOST, PORT


@app.route('/')
def hello_world():
    return redirect("/home")


@app.route("/refresh")
def refresh():
    """更新指令"""
    _apps, _commands = scan_apps()
    execute("DELETE FROM apps")
    execute("DELETE FROM commands")
    execute("UPDATE sqlite_sequence SET seq=0 WHERE name='apps';")
    execute("UPDATE sqlite_sequence SET seq=0 WHERE name='commands';")

    insert_sql_apps = "INSERT INTO apps(appid, appname) VALUES(?,?)"
    executemany(insert_sql_apps, _apps)

    insert_sql_commands = """INSERT INTO commands(name, commands, action, appid) 
        VALUES(?, ?, ?, ?)"""
    executemany(insert_sql_commands, _commands)
    try:
        return render_template("yiwa/refresh.html")
    except:
        return None


@app.route("/reboot")
def reboot():
    """重启web"""

    def _exec(script):
        """执行shell脚本"""
        subprocess.call(script,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    try:
        # 参考1，https://blog.csdn.net/weixin_42840933/article/details/85780125
        # 参考2，https://www.jianshu.com/p/bdfddc6ed505
        _exec("nohup sh ./reboot.sh > ./logs/nohup.log 2>&1 &")
        app.logger.info("重启成功")
    except Exception as error:
        app.logger.error(f"重启失败，报错：{error}")
        # 以下内容可能不会被display
        return "重启失败"
    return "重启成功"


if __name__ == '__main__':
    refresh()
    qr_code.clean_all()
    app.logger.addHandler(Log().handler)
    socketio.run(app, host=HOST, port=PORT)

from apps import app
from flask import request, jsonify, render_template
from apps.__public._sqlite import select
from random import choice

"""伊瓦视图，本应用属于家庭私有使用，不是云端集体部署，功能也是自由切换，就不使用“可插拨视图”功能了。"""


@app.route("/yiwa", methods=["POST"])
def yiwa():
    if request.method == "POST":
        sql = """SELECT status, caption, stt FROM yiwa LIMIT 1"""
        result = select(sql)[0]
        return jsonify(result=result)


@app.route("/commands")
def commands():
    """全部指令"""
    themes = ("default", "primary", "success", "info", "warning", "danger")
    commands = select("""SELECT c.id, c.name, c.commands, a.appid, a.appname 
        FROM commands AS c
        LEFT JOIN apps AS a
        ON c.appid = a.appid
            """)
    apps = {}
    for command in commands:
        key = command.get("appname")
        apps[f"{key}"] = apps.get(f"{key}") if apps.get(f"{key}") else []
        apps[f'{key}'].append(command)
    result, row = [], []
    for id, _apps in enumerate(apps.items(), 1):
        row.append((_apps, choice(themes)))
        if row and (id % 3 == 0):
            result.append(row)
            row=[]
    else:
        if not result and row:
            result.append(row)
    return render_template("yiwa/commands.html", result=result)

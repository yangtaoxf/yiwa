# coding: utf8

"""APPID, APPNAME, COMMANDS三者必须要有
COMMANDS中的目前action分为2种：页面url和包path"""

APPID = "yiwa"
APPNAME = "伊瓦"
COMMANDS = {
    "刷新指令": {
        "commands": ["刷新指令", "更新命令"],
        "action": "/refresh"},
    "显示指令": {
        "commands": ["全部指令", "所有指令", "指令目录", "显示所有指令", "查看所有指令"],
        "action": "/commands"},
    "重启": {
        "commands": ["重启", "重启程序", "重启所有程序"],
        "action": "/reboot"},
    "刷新页面": {
        "commands": ["刷新页面", "重新显示", "刷新"],
        "action": "utils.browser.refresh"},
    "页面向下": {
        "commands": ["向下滚动", "页面向下", "页面下拉"],
        "action": "utils.browser.down"},
    "页面向上": {
        "commands": ["向上滚动", "页面向上", "页面上滚"],
        "action": "utils.browser.up"},
}

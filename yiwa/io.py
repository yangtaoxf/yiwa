# coding: utf8

"""文件读取"""

import os
from importlib import import_module
from yiwa.settings import BASE_DIR


def scan_apps():
    """扫描所有app"""
    apps_path = os.path.join(BASE_DIR, "apps")
    top_dirnames = next(os.walk(apps_path))[1]
    modules = [m for m in top_dirnames if not m.startswith("__")]

    _apps, _commands = [], []
    for module in modules:
        try:
            configs = import_module(f"apps.{module}.configs")
            print(f"成功加载插件配置：apps.{module}.configs")

            _apps.append((configs.APPID, configs.APPNAME))
            for name, command in configs.COMMANDS.items():
                _commands.append((name,
                                  ",".join(command.get("commands")),
                                  command.get("action"),
                                  configs.APPID))
        except ImportError as ierror:
            print("加载插件配置失败或不存在", ierror)

    return (_apps, _commands)

if __name__ == "__main__":
    scan_apps()
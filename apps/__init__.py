# coding: utf8
import os
from flask import Flask, Blueprint
from importlib import import_module

apps_path = __path__[0]


def _app_resource_path(app: str, dir: str):
    """app模板和静态资源路径"""
    return os.path.join(apps_path, app, dir)

# 定义应用
app = Flask(__name__)


# 根目录模块文件夹名称
top_dirnames = next(os.walk(apps_path))[1]
modules = [m for m in top_dirnames if not m.startswith("__")]

# 自动导入所有app资源
for module in modules:
    try:
        # 注册蓝图
        # 参考https://stackoverflow.com/questions/21765692/flask-render-template-with-path
        bp = Blueprint(
            module,
            module,
            url_prefix=f"/{module}",
            template_folder=_app_resource_path(module, "templates"),
            static_folder=_app_resource_path(module, "static"))
        app.register_blueprint(bp)

        # 导入模块
        import_module(f"apps.{module}")
    except ImportError as ierror:
        print("自动导入模块", ierror)

# 注册全局蓝图
bp_public = Blueprint(
    "public",
    "__public",
    url_prefix="/public",
    template_folder=_app_resource_path("__public", "templates"),
    static_folder=_app_resource_path("__public", "static"))
app.register_blueprint(bp_public)

# coding: utf8

"""供插件调用的接口, 说话、消息反馈、生成带二维码的页面等"""

from voice import tts
from yiwa.db import DataConveyor
from tdcode import qr_code
from flask import render_template, request


def say(text):
    """机器对外说话"""
    try:
        tts.say(text)
        return True
    except:
        return False


def feedback(information):
    """信息反馈显示在频幕上"""
    try:
        dc = DataConveyor()
        dc.info(information)
        return True
    except:
        return False


def render_template_with_qrcode(template_name_or_list, **context):
    """生成管理地址二维码，带入到页面"""
    context.update({"qrcode_url": qr_code.make_with_url(request.url)})
    return render_template(template_name_or_list, **context)

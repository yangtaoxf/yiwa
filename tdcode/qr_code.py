# coding: utf8

"""二维码"""

import os
import qrcode
from tdcode.configs import QR_CODE_PATH
from apps import app
from flask import url_for
from yiwa.browser import parse_url


def clean_all():
    """清理所有二维码图片"""
    for file_name in os.listdir(QR_CODE_PATH):
        file_path = os.path.join(QR_CODE_PATH, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def make(data: str, file_name, root_url="/"):
    """
    使用文本数据，制作二维码
    :param data:文本数据
    :param file_name:生成二维码图片的文件名
    :param root_url:返回的url前面的根地址
    :return:二维码图片静态文件url地址
    """
    abs_file_path = os.path.join(QR_CODE_PATH, file_name)

    # 参考https://code.luasoftware.com/tutorials/flask/flask-url-for/
    with app.test_request_context(base_url=root_url):
        qrcode_url = url_for("public.static",
                             filename=f"qrcode/{file_name}",
                             _external=True)
    if os.path.exists(abs_file_path):
        return qrcode_url

    # 参考https://blog.csdn.net/shijichao2/article/details/51228408
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=2
    )
    qr.add_data(data if isinstance(data, str) else "")
    qr.make(fit=True)
    img = qr.make_image()
    img.save(abs_file_path)
    return qrcode_url


def make_with_url(url: str):
    """
    使用url制作二维码
    :param url: 页面相对url路径（例如：http://localhost:5000/cacl/add）
    :return: 二维码静态资源地址
    """
    root_url, url_path = parse_url(url)
    file_name = url_path.replace("/", "_") + ".png"
    return make(url, file_name, root_url)


if __name__ == "__main__":
    print(make("http://localhost:5000/cacl/add"))

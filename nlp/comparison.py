# coding: utf8
"""语音结果和指令比对"""

from aip import AipNlp
from nlp.configs import APP_ID, API_KEY, SECRET_KEY


def match(voice2text, command):
    """匹配指令"""
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    nlp_result_grnn = client.simnet(voice2text, command, {"model": "GRNN"})
    if nlp_result_grnn.get("score", 0.5) >= 0.8:
        return True
    return False


if __name__ == "__main__":
    print(match("关闭设备", "打开设备"))

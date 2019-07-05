# coding: utf8

"""文本转语音"""
import pyttsx3 as pyttsx
from voice.configs import VOICES


# 参考https://github.com/nateshmbhat/pyttsx3
def say(text, voicer=VOICES.get("mei-jia")):
    """说出文稿，缺少对不同平台的处理，例如mac用mei-jia，linux用xxx，windows用xxx"""
    engine = pyttsx.init()
    engine.setProperty("voice", voicer)
    engine.say(text)
    engine.runAndWait()

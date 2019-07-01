# coding: utf8
"""
唤醒，伊瓦，yiwa
尝试用SpeechRecognition库做本地语音识别，避免频繁和百度AI交互，但识别率不高，尤其是中文，大概是数据集是不够。
另外一个ASRT_SpeechRecognition库，数据集特别大6G以上，放弃。
最终采用Pocketsphinx库，字典精简为仅有唤醒词。
"""
import speech_recognition as sr


def up(language="en-US"):
    """SpeechRecognition库本地离线唤醒"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        return r.recognize_sphinx(audio, language=language)
    except Exception as e:
        print(e)
        return ""


import os
from pocketsphinx import get_model_path, AudioFile


def up_ps_audio(wavfile):
    """Pocketsphinx库本地离线唤醒"""
    model_path = get_model_path()

    # lm文件和dict文件替换，参考https://blog.51cto.com/feature09/2300352
    # 所需资源文件在yiwa/asr/resources/中，必需放入到你的/site-packages/pocketsphinx/model/目录下
    config = {
        'verbose': False,
        'audio_file': wavfile,
        'buffer_size': 2048,
        'no_search': False,
        'full_utt': False,
        'hmm': os.path.join(model_path, 'zh_cn'),
        'lm': os.path.join(model_path, '3603.lm'),
        'dict': os.path.join(model_path, '3603.dic')
    }

    # 识别声音文件，参考https://pypi.org/project/pocketsphinx/
    audio = AudioFile(**config)
    for phrase in audio:
        return phrase
    return None


from asr.configs import KEYWORD_FILE


def read_keywords(kwfile=KEYWORD_FILE):
    with open(kwfile) as kf:
        _keywords = kf.readlines()
    return [kw.replace("\n", "") for kw in _keywords]


if __name__ == "__main__":
    # print(up("zh-CN"))
    # up_ps_audio("./output.wav")
    print(read_keywords("./keywords.txt"))

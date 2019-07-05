# coding: utf8
from __future__ import absolute_import
from aip import AipSpeech
from asr.configs import AUDIO_OUTPUT, AUDIO_FORMAT, APP_ID, API_KEY, SECRET_KEY, TIME
from asr.speech import audio_record
from asr.recognition import aip_get_asrresult
from asr.awake import up_ps_audio
from yiwa.log import Log
logger = Log().logger


def listening():
    print("Please say the command")
    audio_record(AUDIO_OUTPUT, TIME)
    asr_result = aip_get_asrresult(AipSpeech(APP_ID, API_KEY, SECRET_KEY),
                                   AUDIO_OUTPUT,
                                   AUDIO_FORMAT)
    return "".join(asr_result) if asr_result else None

def wakeup(keywords: list):
    print("Please wake me up")
    audio_record(AUDIO_OUTPUT, TIME)
    word = up_ps_audio(AUDIO_OUTPUT)
    logger.info(f"尝试唤醒>>> {word}")
    return word, (str(word) in keywords)

if __name__ == "__main__":
    print(listening())

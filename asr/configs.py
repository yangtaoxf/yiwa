# coding: utf8
import pyaudio

APP_ID = "16507144"
API_KEY = "KwAdFdg4nIGKR7vQ6i3ApwOq"
SECRET_KEY = "6PbBUcqjw5fPDnm6p6CDhrAZVspy7sU3"

AUDIO_OUTPUT = "./asr/output.wav"
AUDIO_FORMAT = "wav"
KEYWORD_FILE = "./asr/keywords.txt"

CUID = "18:65:90:cb:f0:51"	# 用户唯一标识，用来区分用户
DEV_PID = 1536	# 普通话(支持简单的英文识别)

CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16bit编码格式
CHANNELS = 1  # 单声道
RATE = 16000  # 16000采样频率

TIME = 3    # 单次录音持续时间，单位：秒
# coding: utf8

import pyaudio
import wave
from asr.configs import CHUNK, FORMAT, CHANNELS, RATE

"""
用Pyaudio库录制音频
	out_file:输出音频文件名
	rec_time:音频录制时间(秒)
"""
def audio_record(out_file, rec_time):

	p = pyaudio.PyAudio()
	# 创建音频流
	stream = p.open(format=FORMAT,  # 音频流wav格式
					channels=CHANNELS,  # 单声道
					rate=RATE,  # 采样率16000
					input=True,
					frames_per_buffer=CHUNK)

	print("Start Recording...")

	frames = []  # 录制的音频流
	# 录制音频数据
	for i in range(0, int(RATE / CHUNK * rec_time)):
		data = stream.read(CHUNK, exception_on_overflow=False)
		frames.append(data)

	# 录制完成
	stream.stop_stream()
	stream.close()
	p.terminate()

	print("Recording Done...")

	# 保存音频文件
	wf = wave.open(out_file, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
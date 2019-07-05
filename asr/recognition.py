# coding: utf8

"""识别语音"""
from aip import AipSpeech
from asr.configs import RATE, CUID, DEV_PID
from yiwa.log import Log

logger = Log().logger

"""读取wav音频文件并返回"""
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

"""
读取paudio录制好的音频文件, 调用百度语音API, 设置api参数, 完成语音识别
    client:AipSpeech对象
    afile:音频文件
    afmt:音频文件格式(wav)
"""
def aip_get_asrresult(client: AipSpeech, afile, afmt):
    print("Waiting...")
    try:
        # 识别结果已经被SDK由JSON字符串转为dict
        result = client.asr(get_file_content(afile), afmt, RATE, {"cuid": CUID, "dev_pid": DEV_PID,})
        # 如果err_msg字段为"success."表示识别成功, 直接从result字段中提取识别结果, 否则表示识别失败
        if result["err_msg"] == "success.":
            return result["result"]
        return []
    except Exception as e:
        logger.error(f"百度语音识别结果：{result}，错误：{e}")
        return []
# coding: utf8

""""""

from selenium import webdriver

CHROMEDRIVER = "./chromedriver"  # chome浏览器selenium驱动路径
STEP = 500  # 滚动的跨度（自行修改，越大滚动条拖动的距离越远）


def create():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-infobars')
    return webdriver.Chrome(executable_path=CHROMEDRIVER)


def refresh(driver):
    """刷新页面"""
    driver.refresh()


# 以下2个方法参考https://www.jianshu.com/p/e2758e830120
def down(driver):
    """向下"""
    driver.execute_script(f"window.scrollBy(0,{STEP})")
    print("down")


def up(driver):
    """向上"""
    driver.execute_script(f"window.scrollBy(0,-{STEP})")
    print("up")

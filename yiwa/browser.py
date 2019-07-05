# coding: utf8

""""""
import os
from selenium import webdriver
from yiwa.settings import BASE_DIR
from urllib.parse import urlparse, urlunparse, urljoin

CHROMEDRIVER = os.path.join(BASE_DIR, "chromedriver")  # chrome浏览器selenium驱动路径
STEP = 500  # 滚动的跨度（自行修改，越大滚动条拖动的距离越远）


def create(driver_path=CHROMEDRIVER):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-infobars')
    return webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)


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


def parse_url(url):
    """解析url，拆分为root和path"""
    # Parse the url to separate out the path
    parsed = urlparse(url)._asdict()
    base_url = f"""{parsed["scheme"]}://{parsed["netloc"]}"""
    return (base_url, parsed["path"])

if __name__ == "__main__":
    browser = create("../chromedriver")
    browser.get("http://www.baidu.com")
    browser.close()
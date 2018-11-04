# coding=utf8
# 라이브러리 가져오기
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re
from urllib.request import urlretrieve

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('log-level=3')

driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)

# 영상 다운로드
def download(video_url):
    driver.get(video_url)
    page_source = driver.page_source
    
    if check_isHD(page_source):
        regex = "hd_src:\"[^\"\s()]+"
        video_source = re.findall(regex, page_source)[0].replace('&amp;', '&').replace('hd_src:"', '')
    else:
        regex = "sd_src:\"[^\"\s()]+"
        video_source = re.findall(regex, page_source)[0].replace('&amp;', '&').replace('sd_src:"', '')

    urlretrieve(video_source, "download.mp4")
    print("다운로드 완료")

# 로그인이 필요한 영상 다운로드
def download_private(video_url):
    print("로그인이 필요한 영상입니다.")
    login_driver = webdriver.Chrome('chromedriver.exe')
    login_driver.get(video_url)

    while True:
        if check_login(video_url, login_driver):
            break
    
    login_driver.get(video_url)
    page_source = login_driver.page_source

    if check_isHD(page_source):
        regex = "hd_src:\"[^\"\s()]+"
        video_source = re.findall(regex, page_source)[0].replace('&amp;', '&').replace('hd_src:"', '')
    else:
        regex = "sd_src:\"[^\"\s()]+"
        video_source = re.findall(regex, page_source)[0].replace('&amp;', '&').replace('sd_src:"', '')

    urlretrieve(video_source, "download.mp4")
    print("다운로드 완료")
    login_driver.quit()
    
# 로그인 여부 확인
def check_login(video_url, login_driver):
    try:
        login_driver.find_element_by_class_name("_1k67")
    except NoSuchElementException:
        return False
    return True

# 로그인이 필요한 영상인지 확인
def check_private(video_url):
    try:
        driver.find_element_by_class_name("login_page")
    except NoSuchElementException:
        return False
    return True

# HD 동영상인지 SD 동영상인지 확인
def check_isHD(page_source):
    regex = "hd_src:[^\\s(),]+"
    if re.findall(regex, page_source)[0] == 'hd_src:null':
        return False
    else:
        return True
    
# 프로그램 메인 함수
if __name__ == '__main__':
    print('Facebook Video Downloader')
    video_url = input('다운로드 하실 영상의 링크를 입력해주세요 : ')
    driver.get(video_url)
    if check_private(video_url):
        download_private(video_url)
    else:
        download(video_url)
    driver.quit()
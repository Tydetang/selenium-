# -*- coding:utf-8 -*-

import re
import requests
import threading
import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs",prefs)

brower = webdriver.Chrome('/Users/tyde/Scripts/Chrome/chromedriver',chrome_options=chrome_options)

wait = WebDriverWait(brower,20)

header = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

def search(keyword,page):
    try:
        brower.get('https://www.google.com.hk/')
    except TimeoutException:
        print 'can not open google!'
    input = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="lst-ib"]')))
    submit = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tsf"]/div[2]/div[3]/center/input[1]')))
    input.send_keys(keyword)
    submit.click()
    get_next(page)

def get_next(page):
    try:
        current_page = get_content()
        if int(current_page) <= page:
            next_page = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pnnext"]/span[2]')))
            next_page.click()
            get_next(page)
        else:
            print 'ok,等待线程结束...'
    except:
        print '没有下一页,等带线程结束...'


def get_content():
    soup = BeautifulSoup(brower.page_source,'lxml')
    for content in soup.find_all(name='div',attrs={'class','srg'}):
        urls = re.findall(r'<a href="(.*?)"',str(content),re.S)
        for url in urls:
            if 'google' not in url:
                t = threading.Thread(target=get_url,args=(url,))
                t.start()
                check_count()
    try:
        page = soup.find_all(name='td',attrs={'class','cur'})
        page = re.findall(r'</span>(.*?)</td>',str(page),re.S)[0]
        print '当前页数:'+page
        print '当前线程数:'+str(threading.active_count())
        return page
    except:
        print '没有下一页,等带线程结束...'

def get_url(url):
    try:
        response = requests.get(url,headers=header)
        if response.status_code ==200:
            print response.url
    except:
        pass

def check_count():
    if threading.active_count()<200:
        # print '线程数:'+str(threading.active_count())
        pass
    else:
        time.sleep(3)
        check_count()

if __name__ == '__main__':
    search('python',100)
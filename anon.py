# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 06:45:12 2021

@author: marle
"""
from selenium.common.exceptions import NoSuchElementException
import string as str
import random
import webbrowser
import string as str
import re
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime
from datetime import date
import numpy as np
from fake_useragent import UserAgent

chrome_driver = '/users/marle/Downloads/ChromeSetUp'

def create_string_of_arbitrary_length(pw, N):        
    pw = ''.join(random.SystemRandom().choice(str.ascii_uppercase + str.digits) for _ in range(N))
    return pw

def prep_browser(path):
    username = ""
    options = webdriver.ChromeOptions()
    ua = UserAgent()
    userAgent = ua.random
    options.add_experimental_option("detach", True)
    options.add_argument("--incognito")
    options.add_argument("--headless")  
    options.add_argument(f'user-agent={userAgent}')
    browser = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
    return browser, username 

browser, username = prep_browser(path = chrome_driver)

def login_to_ig(browser, username, N):
    pw = create_string_of_arbitrary_length(pw = "", N=N)
    browser.get('https://www.instagram.com/f{username}')
    username_element = browser.find_element(By.XPATH, "//input[@name='username']")
    for i in username:
        time.sleep(.15)
        username_element.send_keys(i)
    password_elem = browser.find_element(By.XPATH, "//input[@name='password']")
    for j in pw:
        time.sleep(.15)
        password_elem.send_keys(j)
    browser.find_element(By.XPATH, "//button[contains(.,'Log in')]").click()
    return browser

def looping(browser, username, N):
    for i in range(1,N):
        login_to_ig(browser, username, N=i)
    
def start_trying(browser, username, N):
    while True:
        try:
            looping(browser=browser, username=username, N=N)
            elem = browser.find_element(By.XPATH, "//button[contains(.,'Not Now')]")
            if len(elem) == 0:
                browser.quit()
                time.sleep(50)
                looping(browser, username, N=N)
            if len(elem) != 0:
                grab_url = browser.current_url()
        except NoSuchElementException:
            continue
        break
        
start_trying(browser=browser, username =username, N=15)

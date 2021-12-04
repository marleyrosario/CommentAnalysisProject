# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 18:16:41 2021

@author: marle
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
URL = "https://stacker.com/stories/4225/50-most-popular-democratic-politicians-today"
chrome_driver = '/users/marle/Downloads/chromedriver_win32 (1)/chromedriver'

page = requests.get(URL)

text = page.text
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="block-stacker-content")
names_of_politicians = results.find_all("h2", class_="ct-slideshow__slide__text-container__caption")

names_of_politicians = [name_of_politicians.text for name_of_politicians in names_of_politicians]
names_of_politicians = [re.sub('[^A-Za-z0-9]+', '', name_of_politicians) for name_of_politicians in names_of_politicians]
names_of_politicians = [re.sub(r'[0-9]+', '', name_of_politicians) for name_of_politicians in names_of_politicians]
names_of_politicians = [name_of_politicians.lower() for name_of_politicians in names_of_politicians]
names_of_politicians = names_of_politicians[1:51]

#ig_of_politicians = ["instagram.com/" + name_of_politicians for name_of_politicians in names_of_politicians]
#ig_of_politicians = ["https://" + ig_of_politician for ig_of_politician in ig_of_politicians]

# def replace_instagram_accounts(name_of_politician, username, ig_of_politicians=ig_of_politicians):
#     index_pos_list = [i for i in range(len(ig_of_politicians)) if ig_of_politicians[i] == name_of_politician]
#     ig_of_politicians[index_pos_list[0]] = '"https://"' + "instagram.com/" + username
#     return ig_of_politicians

# replacements = {"harryreid":"senatorreid",
#                 "jacksonlee":"repjacksonlee"}


from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--incognito")
browser = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
browser.get('https://www.instagram.com/aoc')
browser.maximize_window()
account = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys('gavinnewsom')
time.sleep(20)
click_account = browser.find_element(By.XPATH, "//input[@name='Search']").click()
#browsers = [browser.get(ig_of_politician) for ig_of_politician in ig_of_politicians]
# followers = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').text 

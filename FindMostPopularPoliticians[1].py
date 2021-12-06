# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 18:16:41 2021

@author: marle
"""
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

dems = "https://stacker.com/stories/4225/50-most-popular-democratic-politicians-today"
republicans = 'https://stacker.com/stories/4221/50-most-popular-republican-politicians-today'
chrome_driver = '/users/marle/Downloads/chromedriver_win32 (1)/chromedriver'

def find_list_of_politicians(party):
    import requests
    from bs4 import BeautifulSoup
    import re
    page = requests.get(party)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="block-stacker-content")
    names_of_politicians = results.find_all("h2", class_="ct-slideshow__slide__text-container__caption")
    
    names_of_politicians = [name_of_politicians.text for name_of_politicians in names_of_politicians]
    names_of_politicians = [re.sub('[^A-Za-z0-9]+', '', name_of_politicians) for name_of_politicians in names_of_politicians]
    names_of_politicians = [re.sub(r'[0-9]+', '', name_of_politicians) for name_of_politicians in names_of_politicians]
    names_of_politicians = [name_of_politicians.lower() for name_of_politicians in names_of_politicians]
    names_of_politicians = names_of_politicians[1:51]
    return names_of_politicians

def relog_into_instagram():
    username_2 = 'bluejay948'
    password_2 = 'Imtoogood1'
    us = '7737241991'
    pw = 'Imtoogood1!'
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
    browser.get('https://www.instagram.com/')
    browser.maximize_window()
    time.sleep(5)
    username = browser.find_element(By.XPATH, "//input[@name='username']")
    time.sleep(10)
    username.send_keys(username_2)
    password = browser.find_element(By.XPATH, "//input[@name='password']")
    time.sleep(10)
    password.send_keys(password_2)
    browser.find_element(By.XPATH, "//button[contains(.,'Log in')]").click()
    time.sleep(10)
    browser.find_element(By.XPATH, "//input[@name='email']").send_keys(us)
    browser.find_element(By.XPATH, "//input[@name='pass']").send_keys(pw)
    browser.find_element(By.XPATH, "//button[@name='login']").click()
    return browser

def grab_data(browser, name_of_politician):
    account = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
    time.sleep(20)
    account.send_keys(name_of_politician)
    time.sleep(10)
    browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div').click()
    #browsers = [browser.get(ig_of_politician) for ig_of_politician in ig_of_politicians]
    time.sleep(15)
    followers = browser.find_elements_by_class_name("g47SY")
    time.sleep(10)
    current_url = browser.current_url
    followers = followers[1].text
    def convert_thousands_to_number(x):
        import re
        x = x.replace(',', '')
        x = int(x)
        return x
    def convert_str_to_number(x):
        total_stars = 0
        num_map = {'K':1000, 'M':1000000, 'B':1000000000}
        if x.isdigit():
            total_stars = int(x)
        else:
            if len(x) > 1:
                total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
        return int(total_stars)
    
    if "," in followers:
        followers = convert_thousands_to_number(followers)
    else:
        followers = convert_str_to_number(followers)

    df = pd.DataFrame({'URL':current_url, 'Followers':followers}, index=[0])
    time.sleep(100)
    browser.close()
    return df
    
def find_politicians_ig_handles(name_of_politician):
    browser = relog_into_instagram()
    time.sleep(30)
    time.sleep(2.5)
    elem = browser.find_element(By.XPATH, "//button[contains(.,'Not Now')]")
    if len(elem) > 0:
        df = grab_data(browser, name_of_politician)
        time.sleep(100)
        browser.close()
        time.sleep(200)
    else:
        time.sleep(900)
        relog_into_instagram()
        df = grab_data(browser, name_of_politician)
        browser.close()
    return df


def build_csv(dems, republicans):
    dems = find_list_of_politicians(dems)
    republicans = find_list_of_politicians(republicans)
    from selenium.common.exceptions import NoSuchElementException
    list_of_dem_igs=[]
    list_of_republican_igs=[]
    for dem in dems:
        while True:
            try:
                list_of_dem_igs.append(find_politicians_ig_handles(dem))
            except NoSuchElementException:  #spelling error making this code not work as expected
                time.sleep(500)    
                continue
        break
    for republican in republicans:
        while True:
            try:
                list_of_republican_igs.append(find_politicians_ig_handles(republican))
            except NoSuchElementException:  #spelling error making this code not work as expected
                time.sleep(500)    
                continue
        break
    dems = pd.concat(list_of_dem_igs)
    republicans = pd.concat(list_of_republican_igs)
    
    top_5_dems = dems.nlargest(5, 'Followers')
    top_5_republicans = republicans.nlargest(5, 'Followers')
    
    total_list = pd.concat([top_5_dems, top_5_republicans])
    return total_list

total_list = build_csv(dems = dems, republicans = republicans)
total_list.to_csv('C:/Users/marle/Documents/Github/CommentAnalysisProject/total_list.csv')

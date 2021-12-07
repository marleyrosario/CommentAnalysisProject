# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 17:35:09 2021

@author: marle
"""
import pandas as pd
import webbrowser
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import requests

politicians = pd.read_csv('C:/Users/marle/Documents/Github/CommentAnalysisProject/total_list.csv')
chrome_driver = '/users/marle/Downloads/chromedriver_win32 (1)/chromedriver'
path = r"C:\Users\marle\Downloads"

def get_posts(url, agent_id):
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
    time.sleep(30)
    time.sleep(2.5)
    browser.find_element(By.XPATH, "//button[contains(.,'Not Now')]").click()
    phantom_username = 'jacob@mainstreet.one'
    phantom_password = 'Mainstreetone!'
    browser_3 = webdriver.Chrome(chrome_options=options, executable_path = chrome_driver)
    browser_3.get("https://phantombuster.com/5743805120683034/phantoms/6637118561671508/setup/step/connect-to-instagram?returnTo=%2F5743805120683034%2Fphantoms")
    time.sleep(1)
    elem = browser_3.find_element(By.XPATH, "//input[@type='email']" )
    elem_2 = browser_3.find_element(By.XPATH, "//input[@type='password']")
    elem.send_keys(phantom_username)
    elem_2.send_keys(phantom_password)
    time.sleep(2)
    browser_3.find_element(By.XPATH, "//button[contains(.,'Log in')]").click()
    browser_3.maximize_window()
    time.sleep(2)
    session = browser.session_id
    elem_3 = browser_3.find_element(By.XPATH, "//input[@type='text']")
    elem_3.send_keys(Keys.CONTROL + 'a')
    elem_3.send_keys(Keys.DELETE)
    elem_3.send_keys(session)
    time.sleep(2)
    browser_3.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    elem_6 = browser_3.find_element(By.XPATH, "//input[@type='url']")    
    elem_6.send_keys(Keys.CONTROL + 'a')
    elem_6.send_keys(Keys.DELETE)
    url = url
    elem_6.send_keys(url)
    time.sleep(2)   
    browser_3.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(2)
    elem_9 = browser_3.find_element(By.XPATH, "//input[@type='text']")
    elem_9.send_keys(Keys.CONTROL + 'a')
    elem_9.send_keys(Keys.DELETE)
    elem_9.send_keys(url)
    time.sleep(1)
    elem_10 = browser_3.find_element(By.XPATH,"//button[@type='submit']")
    elem_10.send_keys(Keys.PAGE_DOWN)
    elem_10.click()
    browser_3.maximize_window()
    time.sleep(1)
    elem_11 = browser_3.find_element(By.XPATH,"//button[@type='submit']")
    elem_11.send_keys(Keys.PAGE_DOWN)
    elem_11.click()
    time.sleep(3)
    #go to the agent console url and launch phantom
    browser_3.get('https://phantombuster.com/5743805120683034/phantoms/6637118561671508/console')
    time.sleep(2)
    launch = browser_3.find_element(By.XPATH, "//button[@analyticsid='agentLaunchBtn']")
    time.sleep(2)
    launch.click()
    time.sleep(15)
    #Variables set to create an api call
    url = "https://api.phantombuster.com/api/v2/agents/fetch-output"
    querystring = {"id":f'{agent_id}', "mode":"most-recent"}
    time.sleep(25)
    headers = {"Accept": "application/json", 'x-phantombuster-key': "d6wcAtnXbjU3f3akZYFgueSzLi1cDMKvDansjY5AsiA"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    #turn response to json (dictionary in python)
    df = response.json()
    #Grab the output value and create a string variable of all the text from the output of a phantom
    ls = df["output"]
    #create a list grabbing the text that starts with https?://phantom (In an output of the phantom it is structured with 2 urls 1 being the csv file 2 being the json file) list index 0 will always be the csv unless the phantom was rate limited
    link = re.findall(r'(https?://phantom[^\s]+)', ls)
    df = webbrowser.open(link[0]) 
    time.sleep(30)
    browser.close()
    return df

def start_scraping():    
   question = input("Do you want to start scraping? - Y/N:")
   if "Y" in question:
        urls = politicians['URL'].tolist()
        df = [get_posts(url, '6637118561671508') for url in urls]
   else:
        print("Alright. This script is done.")

start_scraping()


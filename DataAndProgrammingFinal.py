# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:42:05 2021

@author: marle
"""

import requests
import pandas as pd
import json
import csv
import os
import glob
import shutil
import io
import webbrowser
import string as str
import re
import urllib
import js2py
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import bigquery_storage
import datetime
from datetime import date
import numpy as np

current_date = datetime.datetime.now()

#create a filename with the date of the current day this is how the program knows which files to grab when running
filename = 'comment_data_' + current_date.strftime("%m") + '_' + current_date.strftime("%d") + '_' + current_date.strftime("%Y"+ '.csv') #current_date.strftime("%d")
filename_2 = 'post_data_' + current_date.strftime("%m") + '_' + current_date.strftime("%d") + '_' + current_date.strftime("%Y" + '.csv')
post_file_name = 'post_data_' + current_date.strftime("%m") + '_' + current_date.strftime("%d") + '_' + current_date.strftime("%Y")
comment_file_name = 'comment_data_' + current_date.strftime("%m") + '_' + current_date.strftime("%d") + '_' + current_date.strftime("%Y")

path_3 = "/Users/marle/Documents/GitHub/mainstreetone_/BQCON/global-cursor-299117-4afbf4e83f5a.json"
path_4 = "/Users/marle/Documents/GitHub/mainstreetone_/BQCON/global-cursor-299117-1ec8eb78ea50.json"
path = f'/Users/marle/Downloads/{filename}'
path_2 = f'/Users/marle/Downloads/{filename_2}'

chrome_driver = '/users/marle/Downloads/chromedriver'

def create_instagram_logins():
    IG_username = input("what would IG username like to add:")
    IG_password = input("what would IG password  like to add:")
    FB_username = input("what would FB username like to add:")
    FB_password = input("what would FB Password like to add:")
    starter_logins = {'Usernames' : ['bluejay948', 'cozy_jay13'],
                    'Passwords' : ['Imtoogood1!', 'TestBestFest1!'],
                    'FB_Usernames' : ['7737241991', 'Test'],
                    'FB_Passwords' : ['Imtoogood1!', 'TestBestFest1!']}
    instagram_logins = starter_logins
    instagram_logins = pd.DataFrame(instagram_logins)
    new_row = {'Usernames': IG_username, 'Passwords':IG_password,
               'FB_Usernames':FB_username, 
               'FB_Passwords': FB_password}    
    instagram_logins = instagram_logins.append(new_row, ignore_index = True)        
    return instagram_logins

instagram_logins = create_instagram_logins()

def add_instagram_logins(instagram_logins):
    IG_username = input("what would IG username like to add:")
    IG_password = input("what would IG password  like to add:")
    FB_username = input("what would FB username like to add:")
    FB_password = input("what would FB Password like to add:")
    new_row = {'Usernames': IG_username, 'Passwords':IG_password,
               'FB_Usernames':FB_username, 
               'FB_Passwords': FB_password}
    instagram_logins = instagram_logins.append(new_row, ignore_index = True)  
    return instagram_logins 

def relog_launch(igusern, igpw, fbun, fbpw, chrome_driver = chrome_driver):
    #calls webdriver adds a couple of arguments and points webdriver to a website
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
    browser.get('https://www.instagram.com')
    
    #logs into instagram
    username_2 = igusern
    password_2 = igpw
    time.sleep(2.5)
    username = browser.find_element(By.XPATH, "//input[@name='username']")
    for i in username_2:
        time.sleep(.15)
        username.send_keys(i)
    password = browser.find_element(By.XPATH, "//input[@name='password']")
    for j in password_2:
        time.sleep(.15)
        password.send_keys(j)
    browser.find_element(By.XPATH, "//button[contains(.,'Log in')]").click()
    
    #login to Facebook as IG's second verification for selenium, once logged in grab session cookie
    us = fbun
    pw = fbpw
    browser.find_element(By.XPATH, "//input[@name='email']").send_keys(us)
    browser.find_element(By.XPATH, "//input[@name='pass']").send_keys(pw)
    browser.find_element(By.XPATH, "//button[@name='login']").click()
    time.sleep(5)
    
    browser.find_element(By.XPATH, "//button[contains(.,'Not Now')]").click()
    session = browser.session_id
    
    #log into phantom buster
    username_3 = 'jacob@mainstreet.one'
    password_3 = 'Mainstreetone!'
    browser_3 = webdriver.Chrome(chrome_options=options, executable_path = chrome_driver)
    browser_3.get("https://phantombuster.com/5743805120683034/phantoms/5148095275855287/setup/step/connect-to-instagram?returnTo=%2F5743805120683034%2Fphantoms")
    time.sleep(1)
    
    elem = browser_3.find_element(By.XPATH, "//input[@type='email']" )
    elem_2 = browser_3.find_element(By.XPATH, "//input[@type='password']")
    elem.send_keys(username_3)
    elem_2.send_keys(password_3)
    time.sleep(2)
    
    browser_3.find_element(By.XPATH, "//button[contains(.,'Log in')]").click()
    time.sleep(2)
    
    #Set up phantom with the session cookie from above ^
    elem_3 = browser_3.find_element(By.XPATH, "//input[@type='text']")
    elem_3.send_keys(Keys.COMMAND + 'a')
    elem_3.send_keys(Keys.DELETE)
    elem_3.send_keys(session)
    time.sleep(2)

    
    browser_3.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    
    elem_6 = browser_3.find_element(By.XPATH, "//input[@type='url']")    
    elem_6.send_keys(Keys.COMMAND + 'a')
    elem_6.send_keys(Keys.DELETE)
    elem_6.send_keys('https://docs.google.com/spreadsheets/d/1TmWrrmaInMfdUAWZVvUh9NEMztP_HsXVgksTUqBvYn4/edit#gid=0')
    time.sleep(2)    
    
    elem_7 = browser_3.find_element(By.XPATH, "//input[@type='text']")
    elem_7.send_keys(Keys.COMMAND + 'a')
    elem_7.send_keys(Keys.DELETE)
    elem_7.send_keys('posts')
    time.sleep(2)
   
    browser_3.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(2)
    
    elem_8 = browser_3.find_element(By.XPATH, "//input[@type='number']")
    elem_8.send_keys(Keys.COMMAND + 'a')
    elem_8.send_keys(Keys.DELETE)
    elem_8.send_keys('')
    time.sleep(2)
    
    elem_9 = browser_3.find_element(By.XPATH, "//input[@type='text']")
    elem_9.send_keys(Keys.COMMAND + 'a')
    elem_9.send_keys(Keys.DELETE)
    elem_9.send_keys('jacob_is_the_best')
    time.sleep(1)
    
    browser_3.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(1)
    browser_3.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(3)
    
    #go to the agent console url and launch phantom
    browser_3.get('https://phantombuster.com/5743805120683034/phantoms/5148095275855287/console')
    time.sleep(2)
    launch = browser_3.find_element(By.XPATH, "//button[@analyticsid='agentLaunchBtn']")
    time.sleep(2)
    launch.click()
    
    #return the session cookie that we grabbed
    return session


def phantom_launch(agent_id):
    url = f"https://api.phantombuster.com/api/v1/agent/{agent_id}/launch"
    headers = {"Accept": "application/json","X-Phantombuster-Key-1": "d6wcAtnXbjU3f3akZYFgueSzLi1cDMKvDansjY5AsiA"}
    response = requests.request("POST", url, headers=headers)
    print(response.text)
    
    #Get the output of the phantom given a phantom id
def get_output(agent_id):
    #Variables set to create an api call
    url = "https://api.phantombuster.com/api/v2/agents/fetch-output"
    querystring = {"id":f'{agent_id}', "mode":"most-recent"}
    headers = {"Accept": "application/json", 'x-phantombuster-key': "d6wcAtnXbjU3f3akZYFgueSzLi1cDMKvDansjY5AsiA"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    #turn response to json (dictionary in python)
    df = response.json()
    #Grab the output value and create a string variable of all the text from the output of a phantom
    ls = df["output"]
    #create a list grabbing the text that starts with https?://phantom (In an output of the phantom it is structured with 2 urls 1 being the csv file 2 being the json file) list index 0 will always be the csv unless the phantom was rate limited
    link = re.findall(r'(https?://phantom[^\s]+)', ls)
    #create a list of the text that starts with Session cookie not valid  anymore.
    check = re.findall(r'(Instagram rate limit reached, you should try again in 15min[^\s]+)', ls)
    #if the length of the list is anything other than 0 than it has been rate limited
    if len(check) != 0:
        #If rate limited then we need to login to instagram and run the phantom in the same browser we logged into instagram
        for i in range(len(instagram_logins)):
            x = relog_launch(igusern= instagram_logins['Usernames'][i], igpw= instagram_logins['Passwords'][i], fbun=instagram_logins['FB_Usernames'][i], fbpw= instagram_logins['FB_Passwords'][i])
            time.sleep(480)
            check, link, i = get_output(agent_id)
            
    else:        
        i = webbrowser.open(link[0])
    
    return check, link, i

check, link, i = get_output('7447948318063011')
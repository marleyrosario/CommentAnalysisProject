# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 17:02:33 2021

@author: marle
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:42:05 2021

@author: marle
"""

from selenium.common.exceptions import NoSuchElementException
import requests
import pandas as pd
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

current_date = datetime.datetime.now()

chrome_driver = '/users/marle/Downloads/chromedriver_win32 (1)/chromedriver'

def create_starter_logins():
    starter_logins = {'Usernames' : ['....', '....'],
                    'Passwords' : ['....', '....'],
                    'FB_Usernames' : ['.....', '....'],
                    'FB_Passwords' : ['.....', '......']}
    instagram_logins = starter_logins
    instagram_logins = pd.DataFrame(instagram_logins)  
    return instagram_logins

instagram_logins = create_starter_logins()

def add_instagram_logins(instagram_logins):
    decision = input("Would you like to add a login to this database - y/n:")
    if decision == 'y':
        IG_username = input("what would IG username like to add:")
        IG_password = input("what would IG password  like to add:")
        FB_username = input("what would FB username like to add:")
        FB_password = input("what would FB Password like to add:")
        new_row = {'Usernames': IG_username, 'Passwords': IG_password,
                   'FB_Usernames':FB_username, 
                   'FB_Passwords': FB_password}
        instagram_logins = instagram_logins.append(new_row, ignore_index = True)
    else:
        print("Alright Great")
    return instagram_logins 

instagram_logins = add_instagram_logins(instagram_logins)

def relog_launch(ig_post, igusern, igpw, fbun, fbpw, chrome_driver = chrome_driver):
    #calls webdriver adds a couple of arguments and points webdriver to a website
    options = webdriver.ChromeOptions()
    ua = UserAgent()
    userAgent = ua.random
    options.add_experimental_option("detach", True)
    options.add_argument("--incognito")
    options.add_argument(f'user-agent={userAgent}')
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
    time.sleep(30)
    
    browser.find_element(By.XPATH, "//button[contains(.,'Not Now')]").click() ### figure out why this isnt working 
    session = browser.session_id
    #log into phantom buster
    username_3 = 'email'
    password_3 = 'password'
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get("create scrape Instagram Phantom on PB WebApp and then put the connect to Instagram link here")    
    time.sleep(1)
    elem = browser.find_element(By.XPATH, "//input[@type='email']" )
    elem_2 = browser.find_element(By.XPATH, "//input[@type='password']")
    elem.send_keys(username_3)
    elem_2.send_keys(password_3)
    time.sleep(2)
    browser.find_element(By.XPATH, "//button[contains(.,'Log in')]").click()
    browser.maximize_window()
    time.sleep(2)
    #Set up phantom with the session cookie from above ^
    elem_3 = browser.find_element(By.XPATH, "//input[@type='text']")
    elem_3.send_keys(Keys.CONTROL + 'a')
    elem_3.send_keys(Keys.DELETE)
    elem_3.send_keys(session)
    time.sleep(2)
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    elem_6 = browser.find_element(By.XPATH, "//input[@type='url']")    
    elem_6.send_keys(Keys.CONTROL + 'a')
    elem_6.send_keys(Keys.DELETE)
    elem_6.send_keys(ig_post)
    time.sleep(2)    
    elem_6.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    browser.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(2)
    time.sleep(2)
    elem_9 = browser.find_element(By.XPATH, "//input[@type='text']")
    elem_9.send_keys(Keys.CONTROL + 'a')
    elem_9.send_keys(Keys.DELETE)
    elem_9.send_keys(ig_post)
    time.sleep(1)
    elem_10 = browser.find_element(By.XPATH,"//button[@type='submit']")
    elem_10.send_keys(Keys.PAGE_DOWN)
    elem_10.click()
    browser.maximize_window()
    time.sleep(1)
    elem_11 = browser.find_element(By.XPATH,"//button[@type='submit']")
    elem_11.send_keys(Keys.PAGE_DOWN)
    elem_11.click()
    time.sleep(3)
    #go to the agent console url and launch phantom
    browser.get('phantom console for comments')
    time.sleep(2)
    launch = browser.find_element(By.XPATH, "//button[@analyticsid='agentLaunchBtn']")
    time.sleep(2)
    launch.click()
    browser.quit()
    #return the session cookie that we grabbed
    return session


def phantom_launch(agent_id):
    url = "https://api.phantombuster.com/api/v1/agent/7447948318063011/launch"
    headers = {"Accept": "application/json","X-Phantombuster-Key-1": "d6wcAtnXbjU3f3akZYFgueSzLi1cDMKvDansjY5AsiA"}
    response = requests.request("POST", url, headers=headers)
    print(response.text)
    
def phantom_call(agent_id):
    url = "https://api.phantombuster.com/api/v2/agents/fetch-output"
    querystring = {"id":'7447948318063011', "mode":"most-recent"}
    headers = {"Accept": "application/json", 'x-phantombuster-key': "d6wcAtnXbjU3f3akZYFgueSzLi1cDMKvDansjY5AsiA"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    #turn response to json (dictionary in python)
    df = response.json()
    return df
     
#Get the output of the phantom given a phantom id
def get_output(agent_id, ig_post):
#Variables set to create an api call
    df = phantom_call(f'{agent_id}')
    #Grab the output value and create a string variable of all the text from the output of a phantom
    if df['isAgentRunning'] is False and df['progress'] >= .20:
        ls = df["output"]
        #create a list grabbing the text that starts with https?://phantom (In an output of the phantom it is structured with 2 urls 1 being the csv file 2 being the json file) list index 0 will always be the csv unless the phantom was rate limited
        link = re.findall(r'(https?://phantom[^\s]+)', ls)
        #create a list grabbing the text that starts with https?://phantom (In an output of the phantom it is structured with 2 urls 1 being the csv file 2 being the json file) list index 0 will always be the csv unless the phantom was rate limited
        link = re.findall(r'(https?://phantom[^\s]+)', ls)
        #create a list of the text that starts with Session cookie not valid  anymore.
        check = re.findall(r'(Instagram rate limit reached, you should try again in 15min[^\s]+)', ls)
        second_check = re.findall(r'(connect to Instagram with this session cookie[^\s]+)', ls)
        couldnt_access = re.findall(r"(Couldn't access input spreadsheet[^\s]+)", ls)
        column_name = re.findall(r"(Incorrect spreadsheet's column name[^\s]+)", ls)    
        #if the length of the list is anything other than 0 than it has been rate limited     
        i = webbrowser.open(link[0])
    elif df['isAgentRunning'] is False and df['progress'] < .20:
        url = "https://api.phantombuster.com/api/v2/agents/fetch-output"
        querystring = {"id":f'{agent_id}', "mode":"most-recent"}
        headers = {"Accept": "application/json", 'x-phantombuster-key': "d6wcAtnXbjU3f3akZYFgueSzLi1cDMKvDansjY5AsiA"}
        response = requests.request("GET", url, headers=headers, params=querystring)
    #turn response to json (dictionary in python)
        df = response.json()
        ls = df["output"]
        #create a list grabbing the text that starts with https?://phantom (In an output of the phantom it is structured with 2 urls 1 being the csv file 2 being the json file) list index 0 will always be the csv unless the phantom was rate limited
        link = re.findall(r'(https?://phantom[^\s]+)', ls)
        #create a list grabbing the text that starts with https?://phantom (In an output of the phantom it is structured with 2 urls 1 being the csv file 2 being the json file) list index 0 will always be the csv unless the phantom was rate limited
        link = re.findall(r'(https?://phantom[^\s]+)', ls)
        #create a list of the text that starts with Session cookie not valid  anymore.
        check = re.findall(r'(Instagram rate limit reached, you should try again in 15min[^\s]+)', ls)
        second_check = re.findall(r'(connect to Instagram with this session cookie[^\s]+)', ls)
        couldnt_access = re.findall(r"(Couldn't access input spreadsheet[^\s]+)", ls)
        column_name = re.findall(r"(Incorrect spreadsheet's column name[^\s]+)", ls)    
        #if the length of the list is anything other than 0 than it has been rate limited
        if len(check) != 0 or len(couldnt_access)!=0 or len(column_name) !=0 or len(second_check) !=0:
            #If rate limited then we need to login to instagram and run the phantom in the same browser we logged into instagram
            for i in range(len(instagram_logins)):
                x = relog_launch(ig_post, igusern= instagram_logins['Usernames'][i], 
                                 igpw= instagram_logins['Passwords'][i], 
                                 fbun=instagram_logins['FB_Usernames'][i], 
                                 fbpw= instagram_logins['FB_Passwords'][i])
                time.sleep(60)
                #check, link, i = get_output(agent_id)     
        else:        
            i = webbrowser.open(link[0])
    elif df['isAgentRunning'] is True:
        time.sleep(180)
        df = phantom_call(f"{agent_id}")
        df = response.json()
        ls = df["output"]
        #create a list grabbing the text that starts with https?://phantom (In an output of the phantom it is structured with 2 urls 1 being the csv file 2 being the json file) list index 0 will always be the csv unless the phantom was rate limited
        link = re.findall(r'(https?://phantom[^\s]+)', ls)
        #create a list grabbing the text that starts with https?://phantom (In an output of the phantom it is structured with 2 urls 1 being the csv file 2 being the json file) list index 0 will always be the csv unless the phantom was rate limited
        link = re.findall(r'(https?://phantom[^\s]+)', ls)
        #create a list of the text that starts with Session cookie not valid  anymore.
        check = re.findall(r'(Instagram rate limit reached, you should try again in 15min[^\s]+)', ls)
        second_check = re.findall(r'(connect to Instagram with this session cookie[^\s]+)', ls)
        couldnt_access = re.findall(r"(Couldn't access input spreadsheet[^\s]+)", ls)
        column_name = re.findall(r"(Incorrect spreadsheet's column name[^\s]+)", ls)    
        #if the length of the list is anything other than 0 than it has been rate limited
        if len(check) != 0 or len(couldnt_access)!=0 or len(column_name) !=0 or len(second_check) !=0:
            #If rate limited then we need to login to instagram and run the phantom in the same browser we logged into instagram
            for i in range(len(instagram_logins)):
                x = relog_launch(ig_post, igusern= instagram_logins['Usernames'][i], 
                                 igpw= instagram_logins['Passwords'][i], 
                                 fbun=instagram_logins['FB_Usernames'][i], 
                                 fbpw= instagram_logins['FB_Passwords'][i])
                time.sleep(60)
                #check, link, i = get_output(agent_id)     
        else:        
            i = webbrowser.open(link[0])
    else:
        ig_post = ig_post.replace("https://", " ")
        webbrowser.open(link[0])
                 

def scrape_comments(agent_id):
    ig_posts = pd.read_csv(r"C:\Users\marle\Documents\Github\CommentAnalysisProject\poststoscrape.csv")
    ig_posts = ig_posts['URL'].tolist()
    for ig_post in ig_posts:
        get_output(f'{agent_id}', ig_post)

scrape_comments()


# -*- coding: utf-8 -*-
"""
Zerodha kiteconnect automated authentication

@author: Arenelli Nikhil Kumar
"""

from kiteconnect import KiteConnect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
from pyotp import TOTP
#"C:\Workspace\alogotrading\Alogotrading.py"

cwd = os.chdir("C:\\Workspace\\alogotrading")
def autologin():
    token_path = "api_key.txt"
    key_secret = open(token_path, 'r').read().split()
    kite = KiteConnect(api_key=key_secret[0])
    service = webdriver.chrome.service.Service(
        executable_path=r"C:\Workspace\alogotrading\chromedriver\chromedriver.exe")
    service.start()
    options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--no-sandbox')
    try:
       driver = webdriver.Chrome(options=options)
   # driver = webdriver.Remote(service.service_url,options)
       driver.get(kite.login_url())
       driver.implicitly_wait(10)

       username = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
       password = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
       username.send_keys(key_secret[2])
       password.send_keys(key_secret[3])
       driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
       
       pin = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input')
       totp = TOTP(key_secret[4])
       token = totp.now()
       print(token)
       pin.send_keys(token)
       time.sleep(10)
    
   
       request_token=driver.current_url.split('request_token=')[1][:32]
       with open('request_token.txt', 'w') as the_file:
           the_file.write(request_token)
        
       print('Successfull logined')
       driver.quit()
    except NameError:
        print("login failed")
        driver.quit()
        


autologin()

#generating and storing access token - valid till 6 am the next day

request_token = open("request_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
data = kite.generate_session(request_token, api_secret=key_secret[1])
with open('access_token.txt', 'w') as file:
        file.write(data["access_token"])

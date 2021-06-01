from numpy import minimum
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import csv
import time

links = ['Brookings/videos','c/FpriOrg/videos',
'c/CNASdc/videos','c/CarnegieEndowment/videos',
'channel/UCwR2e46YHLbPw1k_O3y_qug/videos',
'c/csisdc/videos','user/HooverInstitution/videos',
'c/AtlanticCouncilUS/videos']
PATH = "/home/shashank/Downloads/Web_Scraping/chromedriver"
url = "https://www.youtube.com/"

data = dict()
for i in range(len(links)):
    PATH = "/home/shashank/Downloads/Web_Scraping/Search_Results_Extraction/chromedriver"
    driver = webdriver.Chrome(PATH)
    web_link = url+links[i]
    driver.get(web_link)
    wait = WebDriverWait(driver,15)

    for _ in range(25): # Number of Scroll-Downs
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
    time.sleep(10)
    
    titles = []
    dates=[]
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    date_data = driver.find_elements_by_xpath('//*[@id="metadata-line"]/span[2]')
    #assert len(date_data) == len(user_data), "User and date data unequal"
    #print("Total length of user data: ",len(user_data))
    minimum_n = min(len(user_data),len(date_data))
    for j in range(minimum_n):
        titles.append(user_data[j].get_attribute('title'))
        dates.append(date_data[j].text)
    data[web_link] = {'titles':titles,'dates':dates}
    print(f'Length of rows are: {len(user_data)} for {i}th data')
    #print('*'*100)

    driver.quit()  
    #break

print('Total length of webscraped channels are: ',len(data))

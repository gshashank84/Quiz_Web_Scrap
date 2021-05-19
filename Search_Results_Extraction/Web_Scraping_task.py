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

def extraction(driver):
    souped = BeautifulSoup(driver.page_source, "html.parser")
    ab = souped.find_all('div', {'class': 'search-result-item'})
    #ac = souped.find_all('div', {'class': 'search-result-item'})
    for item in ab:
        ad = item.find_all('h2')
        al = str(item)
            # print(al)
            # af = .get_text()
        ah = item.find_all('p')
        for items, heads in zip(ad, ah):
            title = items.get_text()
            content = heads.get_text()
            print(title)
            print(content)

df = pd.read_csv('sample_data_ketan_26_feb_2021.csv')
#df1 = df.style.hide_index()
split_values = df['Search Term'].unique()
#print(split_values)
for x in range(len(split_values)):
    #print(split_values[x])
    PATH = "/home/shashank/Downloads/Web_Scraping/chromedriver"
    driver = webdriver.Chrome(PATH)
    url = "https://www.sfo.gov.uk"
    driver.get(url)
    time.sleep(1)
    search = driver.find_element_by_id("s")
    if (search is not None):
        search.send_keys(split_values[x])
        search.send_keys(Keys.RETURN)
        
        extraction(driver)       
        while(True):
            try:
                driver.find_element_by_link_text("Next »").click()
                extraction(driver)
            except:
                break
         
    driver.quit()
         
         





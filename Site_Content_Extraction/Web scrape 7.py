import requests
from bs4 import BeautifulSoup
import os
from pycountry import countries
url = 'https://www.countryflags.io'
folder1 ='CountryFlags5'
folder2 ='CountryFlags6'

def imagedown(url,folder1,folder2):
    try:
        os.mkdir(folder1)
    except:
        print('Folder1 already created')
    try:
        os.mkdir(folder2)
    except:
        print('Folder2 already created')
    
    page = requests.get(url)
    souped = BeautifulSoup(page.content, "html.parser")
    all = souped.find_all("div", {"class": "item_country"})
    imgs = souped.find_all("img", {"class": "theme-flat"})
    a1 = len(imgs)
    i = 1
    for img, item in zip(imgs, all):
        imglink = img.attrs.get("src")
        image = requests.get(url + imglink).content
        Alt = item.find("p")
        AA = Alt.get_text()
        filename = AA + ".png"
        AB = countries.get(alpha_2=AA)
        if AB is not None:
            AC = AB.alpha_3
            filename1 = AC + ".png"
            if i <= a1:
                with open(folder1+'/'+filename, "wb") as file:
                    file.write(image)
                
                with open(folder2+'/'+filename1, "wb") as file:
                    file.write(image)
                
                i += 1
            else:
                file.close()
                break
            
        else:
            continue
            
imagedown(url,folder1,folder2)
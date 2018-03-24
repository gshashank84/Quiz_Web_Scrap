#lets write a Simple script 
#to get the 20 words and their frequency percentage 
#with highest frequency in an English Wikipedia article. 
#applications are recommender systems, chatbots and NLP, sentiment analysis,
#data visualization,
#market research

#Beautiful Soup is a Python library 
#for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup
#Requests is one of the most downloaded 
#Python packages of all time, 
#pulling in over 7,000,000 downloads every month.
#HTTP library for pulling pushing and authenticating
import requests
#lets you do Regular expression operations
#special text string for describing a search pattern.
#find and replace
import re
#The operator module exports a 
#set of efficient functions 
#corresponding to the intrinsic operators of Python.
#comparison, addition, greater than less then
import operator
#parses json, formats it
import json
#The module provides just one function, 
#tabulate, which takes a list of lists or another 
#tabular data type as the first argument, 
#and outputs a nicely formatted plain-text table:
from tabulate import tabulate
#system calls, dealw with user arguments
import sys
#list of common stop words various languages like the
from stop_words import get_stop_words

from urllib.request import Request, urlopen

from selenium import webdriver

from requests import get
from pattern.web import plaintext

from PIL import Image
import pytesseract

driver= webdriver.Chrome("F:\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver.get("http://192.168.43.1:8080")

while True:
    #driver.implicitly_wait(2)
    driver.maximize_window()
    driver.get_screenshot_as_file("Screenshot.png")
    im = Image.open("Screenshot.png")
    text = pytesseract.image_to_string(im, lang = 'eng')
    if(len(text) > 5):
        driver.quit()
        break
    else:
        print("Unable to scan the screen")


print(text)

#access wiki API. json format. query it for data. search tyep. shows list of possibilities
google_api_link = "http://www.google.com/search?q="

# String_query Classifier
s = text.replace('\n','')
n = s
for i in range(0,len(s)):
    if n.startswith(('Wh','The','On','In','who','how')):
        s = n
        break
    else:
        n = s[i:]

for i in range(0,len(s)):
    if n.endswith(('?')):
        s = n
        break
    else:
        n = s[:i]

string_query = s
print(string_query)

#Options Classifier
try:
    text = text[text.index('?')+1:]
except:
    text = text[text.index('.')+1:]
    
if len(text)< 5:
    print('/////Options are not recognized')
    driver= webdriver.Chrome("F:\\Downloads\\chromedriver_win32\\chromedriver.exe")
    driver.get(google_api_link + s)
    exit()
else:
    y = text.replace("\n",'-')
    j = y.split('-')
    j.reverse()
    options_list = []
    for i in range(0,len(j)):
        if j[i] == '':
            continue
        else:
            if len(options_list) == 3:
                break
            else:
                options_list.append(j[i])


"""j = s
for i in range(0,len(s)):
    if j.startswith(('?')):
        break
    else:
        j = s[i:]

options_book = j[1:]
options_list = options_book.split()"""





#create our URL
url = google_api_link + string_query

#get the words
def getWordList(url):
    word_list = []
    #raw data
    #source_code = requests.get(url)
    #convert to text
    #plain_text = source_code.text
    #lxml format
   # soup = BeautifulSoup(plain_text,'lxml')

    htmlString = get(url).text
    webText = plaintext(htmlString)

    #find the words in paragraph tag
    #for text in webText.findAll('p'):
        #if text.text is None:
        #    continue
        #content
       # content = text.text
        #lowercase and split into an array
    words = webText.lower().split()

        #for each word
    for word in words:
        #remove non-chars
        cleaned_word = clean_word(word)
        #if there is still something there
        if len(cleaned_word) > 0:
            #add it to our word list
            word_list.append(cleaned_word)

    return word_list


#clean word with regex
def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', '', word)
    return cleaned_word


def createFrquencyTable(word_list):
   #the arguments should not be float value

    for i in range(0,len(options_list)):
        options_list[i] = options_list[i].lower()

   # options = {sys.argv[1]:0, sys.argv[2]:0}

    options = {}
    for i in range(0,len(options_list)):
        options[options_list[i]] = 0


    x = [x for x in options.keys()]
    # x  = ['option1', 'option2']

    for n in x:
        if " " in n:
            for word in word_list:
                if word in n:
                    options[n] += 1
        else:
            for word in word_list:
                if word in options:
                    options[word] += 1
   #     else:
   #        word_count[word] = 1
    return options

#remove stop words
def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')

    temp_list = []
    for key,value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list


#wikipedia_link = "http://www.google.com/search?q="

#if the search word is too small, throw error
"""if(len(options_list) < 1):
    print("Total options wasn't scanned")
    exit()"""

#get the search word
#string_query = sys.argv[1]

search_mode = True

#to remove stop words or not
"""if(len(sys.argv) > 2):
    search_mode = True
else:
    search_mode = False"""



#try-except block. simple way to deal with exceptions 
#great for HTTP requests
try:
    #use requests to retrieve raw data from wiki API URL we
    #just constructed
   # response = requests.get(url)


    """req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    raw_data = web_byte.decode('utf-8')
    wikipedia_page_tag = json.loads(raw_data)"""

    #format that data as a JSON dictionary
    #data = json.loads(response.content.decode("utf-8"))

    #page title, first option
    #show this in web browser
    #wikipedia_page_tag = data['query']['search'][0]['title']

    #get actual wiki page based on retrieved title
    #url = wikipedia_link + wikipedia_page_tag

    

    #get list of words from that page
    page_word_list = getWordList(url)
    #create table of word counts, dictionary
    page_word_count = createFrquencyTable(page_word_list)

    s = [s for s in page_word_count.values()]

    if s[0]==0 and s[1]==0 and s[2]==0:
        driver= webdriver.Chrome("F:\\Downloads\\chromedriver_win32\\chromedriver.exe")
        driver.get(url)
        url = driver.find_element_by_xpath("""//*[@id="taw"]/div[2]/div/p/a""").get_attribute("href")
        page_word_list = getWordList(url)
        page_word_count = createFrquencyTable(page_word_list)

    #sort the table by the frequency count
    if "NOT" in string_query:
        sorted_word_frequency_list = sorted(page_word_count.items(), key=operator.itemgetter(1), reverse=True)
        sorted_word_frequency_list.reverse()
        print("NOT STATEMENT")
    else:
        sorted_word_frequency_list = sorted(page_word_count.items(), key=operator.itemgetter(1), reverse=True)
    
    #remove stop words if the user specified
    #if(search_mode):
     #   sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

    #sum the total words to calculate frequencies   
    #total_words_sum = 0
    #for key,value in sorted_word_frequency_list:
     #   total_words_sum = total_words_sum + value

    #just get the top 20 words
    #if len(sorted_word_frequency_list) > 20:
     #   sorted_word_frequency_list = sorted_word_frequency_list[:20]

    #create our final list which contains words, frequency (word count), percentage
    final_list = []
    for key,value in sorted_word_frequency_list:
        percentage_value = float(value * 100) / (len(options_list))
        final_list.append([key, value, round(percentage_value, 4)])

    #headers before the table
    print_headers = ['Word', 'Frequency', 'Frequency Percentage']

    #print the table with tabulate
    print(tabulate(final_list, headers=print_headers, tablefmt='orgtbl'))

#throw an exception in case it breaks
except requests.exceptions.Timeout:
    print("The server didn't respond. Please, try again later.")


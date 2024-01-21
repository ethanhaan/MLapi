import sys
from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import requests
import time

from web_scraper_functions import *

searchQuery = "apple"
num_results = 10
page_contents = []

urls = search_google_news(searchQuery)

print(urls)

page_contents = []

for url in urls:
    page_content = get_page_content(url)
    if(page_content == False):
        driver = webdriver.Chrome(options=options)
    else:	
        page_contents.append(page_content)


# Merge all page contents
news_string = ""
for page in page_contents:
    for paragraph in page:
        news_string = f"{news_string}\n{paragraph}" 
    news_string+="\n"

print(news_string)

driver.quit()

exit(1)

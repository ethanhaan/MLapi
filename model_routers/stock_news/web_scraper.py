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
from datetime import datetime
import threading
import requests
import time

from model_routers.stock_news.web_scraper_functions import *

def scrape_web(task, search_query, limit, save_tasks_to_file):

    task["time_started"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    task["urls"] = search_google_news(search_query)[:limit]

    for url in task["urls"]:
        page_content = get_page_content(url)
        if(page_content == False):
            driver = webdriver.Chrome(options=options)
        else:	
            task["page_contents"].append(page_content)
        save_tasks_to_file()

    # Merge all page contents
    news_string = ""
    for page in task["page_contents"]:
        for paragraph in page:
            news_string = f"{news_string}\n{paragraph}" 
        news_string+="\n"

    task["status"] = "COMPLETE"
    task["result"] = news_string
    save_tasks_to_file()


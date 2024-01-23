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

def setup_webdriver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    options.add_argument("--no-sandbox")  # Bypass OS security model, necessary on some systems
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(6)
    return driver

def search_google_news(query):
    driver = setup_webdriver()
    driver.get("https://www.google.com/")
    time.sleep(1)
    search_bar = driver.find_element(By.CSS_SELECTOR, "textarea")
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(1)
    news_span = driver.find_element(By.XPATH, "//span[contains(text(), 'News')]")
    news_anchor = news_span.find_element(By.XPATH, "./../..")
    news_anchor.click()
    time.sleep(1)
    anchor_elements = driver.find_elements(By.XPATH, "//a[@href]")
    href_values = [element.get_attribute('href') for element in anchor_elements if "google.com" not in element.get_attribute("href")]
    driver.quit()
    return href_values

def load_page(driver, url, timeout, paragraphs):
    try:
        driver.get(url)
        time.sleep(timeout)
    except Exception as e:
        print(f"Error during page load: {e}")
    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        p_tags = soup.find_all('p')
        for paragraph in p_tags:
            paragraphs.append(paragraph.get_text())
        driver.quit()

def get_page_content(url):

    driver = setup_webdriver()
    paragraphs = []

    thread = threading.Thread(target=load_page, args=(driver, url, 6, paragraphs))
    thread.start()
    thread.join(timeout=10)

    if thread.is_alive():
        print("Operation timed out. The browser will be closed.")
        driver.quit()  
    print(paragraphs)
    return paragraphs 

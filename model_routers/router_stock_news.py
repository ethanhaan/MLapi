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


def get_page_content(driver, url):

		def load_url():
				driver.set_page_load_timeout(6)
				driver.get(url)

		try:
				# The web driver is waiting for the condition document.readyState === 'complete' to be true
				# Start load_url() in a separate thread so forcefully terminate if stuck
				load_thread = threading.Thread(target=load_url)
				load_thread.start()
				print("ENDING THREAD")
				load_thread.join(timeout=7)

				if(load_thread.is_alive()):
						print("FORCEFULLY TIMED OUT")
						driver.quit()
						return False

		except:
				print("TIMED OUT WAITING FOR PAGE TO LOAD")

		content = driver.page_source
		soup = BeautifulSoup(content, 'html.parser')
		return soup.find_all('p')


query = "apple"
num_results = 10
page_contents = []

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--enable-logging")
options.add_argument("--v=1")
options.add_argument("--no-sandbox")  # Bypass OS security model, necessary on some systems
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

driver = webdriver.Chrome(options=options)

url = "https://reuters-business-and-financial-news.p.rapidapi.com/article-date/2024-01-06"

headers = {
	"X-RapidAPI-Key": "3236932a7bmshf8407f9adbd57a7p1734d2jsn1025ad3deb42",
	"X-RapidAPI-Host": "reuters-business-and-financial-news.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())
exit(1)

urls = [article["url"] for article in news_results.json()][:num_results]
print(urls)
for url in urls:
		print("GETTING PAGE CONTENT")
		page_content = get_page_content(driver, url)
		if(page_content == False):
				driver = webdriver.Chrome(options=options)
		else:	
				page_contents.append(page_content)

print(page_contents)


driver.quit()


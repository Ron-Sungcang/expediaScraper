from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

PATH = 'C:/Program Files (x86)/chromedriver-win64/chromedriver.exe'

options = webdriver.ChromeOptions()

options.add_argument('Chrome/122.0.4280.141')
options.add_argument('accept-encoding=gzip, deflate, br')
options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
options.add_argument('referer=https://www.expedia.com/')
options.add_argument('upgrade-insecure-requests=1')

cityName = input("What city are you staying at?")
target_url = ("https://www.expedia.ca/")


driver = webdriver.Chrome(options=options)
driver.get(target_url)

# Search for cities
button = driver.find_element(By.XPATH,'//button[@data-stid="destination_form_field-dialog-trigger"]')
driver.implicitly_wait(10)
button.click()
citySearch = driver.find_element(By.XPATH,'//input[@id="destination_form_field"]')
driver.implicitly_wait(10)
citySearch.click()
citySearch.send_keys(cityName)
driver.implicitly_wait(10)
citySearch.send_keys(Keys.ENTER)

time.sleep(5)

resp = driver.page_source
driver.close()
print(resp)
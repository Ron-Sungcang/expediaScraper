from bs4 import BeautifulSoup
from selenium import webdriver
import time

PATH = 'C:/Program Files (x86)/chromedriver-win64/chromedriver.exe'

options = webdriver.ChromeOptions()

options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/87.0.4280.141 Mobile Safari/537.36')
options.add_argument('accept-encoding=gzip, deflate, br')
options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
options.add_argument('referer=https://www.expedia.com/')
options.add_argument('upgrade-insecure-requests=1')

target_url = ("https://www.expedia.ca/")


driver = webdriver.Chrome(options=options)

driver.get(target_url)

time.sleep(5)

resp = driver.page_source
driver.close()
print(resp)
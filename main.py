import calendar

from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from datetime import datetime

PATH = 'C:/Program Files (x86)/chromedriver-win64/chromedriver.exe'

options = webdriver.ChromeOptions()

options.add_argument('Chrome/122.0.4280.141')
options.add_argument('accept-encoding=gzip, deflate, br')
options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
options.add_argument('referer=https://www.expedia.ca/')
options.add_argument('upgrade-insecure-requests=1')

cityName = input("What city are you staying at?")
startDate = input("Enter date to check in: Format = YYYY/MM/DD")
startDate = startDate.split("/")
year_start = int(startDate[0])
month_start = int(startDate[1])
day_start = int(startDate[2])
endDate = input("Enter date to check out: Format = YYYY/MM/DD")
endDate = endDate.split("/")
year_end = int(endDate[0])
month_end = int(endDate[1])
day_end = int(endDate[2])
no_of_travellers = int(input("Number of travellers?"))
no_of_children = int(input("Number of children?"))
age_of_child = []
if no_of_children > 0:
    age_of_child = input("How old are your children?: Format = AGE1/AGE2")
    age_of_child = age_of_child.split("/")
    age_of_child = list(map(int, age_of_child))

target_url = "https://www.expedia.ca/"

driver = webdriver.Chrome(options=options)
driver.get(target_url)


def row_col_date(year, month, day):
    """
    A helper function that helps calculate the row, column, and month index to be put in the
    WebDriver methods to select the right date
    :param year: Year represented in int
    :param month: Month represented in int
    :param day: Day represented in Int
    :return: A list of ints that represents row, column, and month index
    """

    # Calculation for row and column
    starting_day = calendar.monthrange(year, month)[0]
    specific_day = (starting_day + day - 1) % 7
    row = (starting_day + day - 1) // 7 + 1
    col = specific_day + 2

    # Calculations for month index
    current_date = datetime.now()
    current_month = current_date.month
    month_index = month - current_month + 1
    return [month_index, row, col]


# These guys are going to be put in the main function
start_date = row_col_date(year_start, month_start, day_start)
end_date = row_col_date(year_end, month_end, day_end)


def search_for_cities(city_info, driver_use):
    """
    Uses Selenium to enter a city into the Expedia city search. Finds the search button for the city search
    and uses a for loop to enter the name of the city
    :param city_info: A string to enter into the search bar
    :param driver_use: A webdriver
    :return: null
    """
    city_button = driver_use.find_element(By.XPATH, '//button[@data-stid="destination_form_field-dialog-trigger"]')
    time.sleep(5)
    city_button.click()
    city_search = driver_use.find_element(By.XPATH, '//input[@id="destination_form_field"]')
    time.sleep(5)
    city_search.click()
    for i in city_info:
        city_search.send_keys(i)
        time.sleep(1)
    city_search.send_keys(Keys.ENTER)


def select_date(driver_use, start_list, end_list):
    """
    Uses Selenium to enter a check-in date and a check-out date, takes a list of int values to
    make sure that the proper buttons are selected
    :param driver_use: A webdriver
    :param start_list: A list of ints that represents row, column, and month index
    :param end_list: A list of ints that represents row, column, and month index
    :return: null
    """
    date_button = driver_use.find_element(By.XPATH, '//button[@data-stid="uitk-date-selector-input1-default"]')
    date_button.click()
    time.sleep(10)
    start_date_button = driver_use.find_element(By.XPATH,
                                                f'//div[{start_list[0]}]/table/tbody/tr[{start_list[1]}]/td[{start_list[2]}]')
    start_date_button.click()
    time.sleep(5)
    end_date_button = driver_use.find_element(By.XPATH,
                                              f'//div[{end_list[0]}]/table/tbody/tr[{end_list[1]}]/td[{end_list[2]}]')
    end_date_button.click()
    time.sleep(5)
    apply_date_button = driver_use.find_element(By.XPATH, '//button[@data-stid="apply-date-selector"]')
    apply_date_button.click()


def select_travelers(driver_use, travellers, children, child_age_list):
    """
    Uses Selenium to enter the amount of travellers looking to check in. For the traveller side of the calculation
    this uses a for loop to click the plus button in expedia. For the children age side, uses a for loop to put the
    right Xpath to the child age selectors
    :param driver_use: Selenium WebDriver
    :param travellers: an int that represents the amount of travellers
    :param children: an int that represents the amount of children
    :param child_age_list: a list of the age of the children
    :return: null
    """
    travel_button = driver_use.find_element(By.XPATH, '//button[@data-stid="open-room-picker"]')
    travel_button.click()
    time.sleep(5)
    add_travel = driver_use.find_element(By.XPATH, '//div/div/button[2]')
    sub_travel = driver_use.find_element(By.XPATH, '//section/div[1]/div[1]/div/div/button[1]')
    add_child = driver_use.find_element(By.XPATH, '//section/div[1]/div[2]/div[1]/div/button[2]')

    if travellers == 1:
        sub_travel.click()
    elif travellers > 2:
        for i in range(2, travellers):
            add_travel.click()
            time.sleep(1)

    if children > 0:
        for i in range(0, children):
            add_child.click()
            time.sleep(1)

        for j in range(0, len(child_age_list)):
            child_age_button = driver.find_element(By.XPATH, '//select['
                                                             '@id="age-traveler_selector_children_age_selector-0'
                                                             f'-{j}"]')
            child_age_button.click()
            time.sleep(2)
            child_age_selector = driver.find_element(By.XPATH, '//select['
                                                               '@id="age-traveler_selector_children_age_selector-0'
                                                               f'-{j}"]/option[{child_age_list[j] + 2}]')
            child_age_selector.click()
    time.sleep(2)
    done_button = driver.find_element(By.XPATH, '//button[@id="traveler_selector_done_button"]')
    done_button.click()


search_for_cities(cityName, driver)

select_date(driver, start_date, end_date)

select_travelers(driver,no_of_travellers,no_of_children,age_of_child)

print(len(age_of_child))
time.sleep(5)

driver.close()

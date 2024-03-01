import calendar
import re
import csv

from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from datetime import datetime

PATH = 'C:/Program Files (x86)/chromedriver-win64/chromedriver.exe'


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


def search_for_cities(city_info, driver_use):
    """
    Uses Selenium to enter a city into the Expedia city search. Finds the search button for the city search
    and uses a for loop to enter the name of the city
    :param city_info: A string to enter into the search bar
    :param driver_use: A webdriver
    :return: null
    """
    city_button = driver_use.find_element(By.XPATH, '//button[@data-stid="destination_form_field-dialog-trigger"]')
    time.sleep(2)
    city_button.click()
    city_search = driver_use.find_element(By.XPATH, '//input[@id="destination_form_field"]')
    time.sleep(2)
    city_search.click()
    for i in city_info:
        city_search.send_keys(i)
        time.sleep(0.25)
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
    time.sleep(5)
    start_date_button = driver_use.find_element(By.XPATH,
                                                f'//div[{start_list[0]}]/table/tbody/tr[{start_list[1]}]/td[{start_list[2]}]')
    start_date_button.click()
    time.sleep(2)
    end_date_button = driver_use.find_element(By.XPATH,
                                              f'//div[{end_list[0]}]/table/tbody/tr[{end_list[1]}]/td[{end_list[2]}]')
    end_date_button.click()
    time.sleep(2)
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
    time.sleep(2)
    travel_button.click()
    time.sleep(2)
    add_travel = driver_use.find_element(By.XPATH, '//*[@id="lodging_search_form"]/div/div/div[3]/div/div['
                                                   '2]/div/div/section/div[1]/div[1]/div/div/button[2]')
    sub_travel = driver_use.find_element(By.XPATH, '//*[@id="lodging_search_form"]/div/div/div[3]/div/div['
                                                   '2]/div/div/section/div[1]/div[1]/div/div/button[1]')
    add_child = driver_use.find_element(By.XPATH, '//*[@id="lodging_search_form"]/div/div/div[3]/div/div['
                                                  '2]/div/div/section/div[1]/div[2]/div[1]/div/button[2]')

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
            child_age_button = driver_use.find_element(By.XPATH, '//select['
                                                                 '@id="age-traveler_selector_children_age_selector-0'
                                                                 f'-{j}"]')
            time.sleep(2)
            child_age_button.click()
            time.sleep(2)
            child_age_selector = driver_use.find_element(By.XPATH, '//select['
                                                                   '@id="age-traveler_selector_children_age_selector-0'
                                                                   f'-{j}"]/option[{child_age_list[j] + 2}]')
            child_age_selector.click()
    time.sleep(2)
    done_button = driver_use.find_element(By.XPATH, '//button[@id="traveler_selector_done_button"]')
    done_button.click()


def webscrape(option_use, target_url, year_start, month_start, day_start, year_end, month_end, day_end, city_name,
              no_of_travellers, no_of_children, age_of_child):
    """
    Navigates to the expedia website and navigates through the selection process using
    navigating functions in this script. Scrapes the website for hotel name, address, rating
    price per day, and the final price. Puts these items in a dictionary
    :param age_of_child:
    :param no_of_children:
    :param no_of_travellers:
    :param city_name:
    :param day_end:
    :param month_end:
    :param year_end:
    :param day_start:
    :param month_start:
    :param year_start:
    :param target_url:
    :param option_use: ChromeOptions to be used by the driver
    :return: a dictionary consisting of keys and list values
    """
    hotel_name_list = list()
    hotel_address_list = list()
    hotel_price_before = list()
    hotel_price_after = list()
    hotel_ratings = list()
    hotel_link = list()
    hotel_dictionary = {}

    driver = webdriver.Chrome(options=option_use)
    driver.get(target_url)
    time.sleep(5)
    close_button = driver.find_element(By.XPATH, '//body/div[1]/div[1]/div[2]/section/div[2]/button')
    close_button.click()

    checkin_date = row_col_date(year_start, month_start, day_start)
    checkout_date = row_col_date(year_end, month_end, day_end)

    search_for_cities(city_name, driver)
    select_date(driver, checkin_date, checkout_date)
    select_travelers(driver, no_of_travellers, no_of_children, age_of_child)

    finish_button = driver.find_element(By.XPATH, '//button[@id="search_button"]')
    finish_button.click()

    # Human must handle captcha manually
    # Tells selenium to pause until user finishes captcha
    input('Press enter after captcha is resolved')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    resp = driver.page_source

    # Scrapes the website when in the proper page
    soup = BeautifulSoup(resp, 'html.parser')
    all_hotels = soup.find("div", {"data-stid": "property-listing-results"})
    hotels = all_hotels.find_all("div", {"class": "uitk-spacing uitk-spacing-margin-blockstart-three"})

    for hotel in hotels:
        hotel_arr = hotel.find("div", {
            "class": "uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column "
                     "uitk-layout-flex-justify-content-space-between"})
        try:
            name = hotel_arr.find("h3").text
            hotel_name_list.append(name)
        except:
            pass

        try:
            prices = hotel_arr.find("div", {"data-test-id": "price-summary"}).text
            price_lis = re.sub(r"[^0-9,]", " ", prices)
            price_lis = " ".join(price_lis.split())
            price_lis = price_lis.split(" ")
            price_no_dupl = []
            [price_no_dupl.append(price) for price in price_lis if price not in price_no_dupl]

            if len(price_no_dupl) == 2:
                hotel_price_before.append(int(price_no_dupl[0].replace(',', '')))
                hotel_price_after.append(int(price_no_dupl[1].replace(',', '')))
            else:
                hotel_price_before.append(int(price_no_dupl[1].replace(',', '')))
                hotel_price_after.append(int(price_no_dupl[2].replace(',', '')))
        except:
            pass

        try:
            address_list = hotel_arr.find_all("div", {
                "class": "uitk-text uitk-text-spacing-half truncate-lines-2 uitk-type-300 uitk-text-default-theme"})
            if len(address_list) == 1:
                hotel_address_list.append(address_list[0].text)
            else:
                hotel_address_list.append(address_list[1].text)
        except:
            pass

        try:
            rating = hotel_arr.find("span", {"class": "uitk-badge-base-text"}).text
            hotel_ratings.append(float(rating))
        except:
            pass

        try:
            link_find = hotel.find("a", {"data-stid": "open-hotel-information"}).get("href")
            link = link_find.replace('/', target_url, 1)
            hotel_link.append(link)
        except:
            pass

    hotel_dictionary["Hotel Name"] = hotel_name_list
    hotel_dictionary["Address"] = hotel_address_list
    hotel_dictionary["Price Per Day"] = hotel_price_before
    hotel_dictionary["Final Price"] = hotel_price_after
    hotel_dictionary["Rating"] = hotel_ratings
    hotel_dictionary["Link"] = hotel_link

    driver.close()
    return hotel_dictionary


def output_to_csv(dictionary, sort):
    """
    Sorts a dictionary depending on user preference then outputs a csv file
    :param dictionary: dictionary to be sorted and used to write csvfile
    :param sort: user's sorting preference
    :return: null
    """
    # Sort using what the user wanted
    match sort:
        case "lowestperday":
            dictionary["Hotel Name"] = [x for _, x in
                                        sorted(zip(dictionary["Price Per Day"], dictionary["Hotel Name"]))]
            dictionary["Final Price"] = [x for _, x in
                                         sorted(zip(dictionary["Price Per Day"], dictionary["Final Price"]))]
            dictionary["Address"] = [x for _, x in sorted(zip(dictionary["Price Per Day"], dictionary["Address"]))]
            dictionary["Rating"] = [x for _, x in sorted(zip(dictionary["Price Per Day"], dictionary["Rating"]))]
            dictionary["Link"] = [x for _, x in sorted(zip(dictionary["Price Per Day"], dictionary["Link"]))]
            dictionary["Price Per Day"] = sorted(dictionary["Price Per Day"])
        case "lowestfinal":
            dictionary["Hotel Name"] = [x for _, x in sorted(zip(dictionary["Final Price"], dictionary["Hotel Name"]))]
            dictionary["Price Per Day"] = [x for _, x in sorted(zip(dictionary["Final Price"], dictionary["Price Per "
                                                                                                          "Day"]))]
            dictionary["Address"] = [x for _, x in sorted(zip(dictionary["Final Price"], dictionary["Address"]))]
            dictionary["Rating"] = [x for _, x in sorted(zip(dictionary["Final Price"], dictionary["Rating"]))]
            dictionary["Link"] = [x for _, x in sorted(zip(dictionary["Final Price"], dictionary["Link"]))]
            dictionary["Final Price"] = sorted(dictionary["Final Price"])
        case "lowestrating":
            dictionary["Hotel Name"] = [x for _, x in sorted(zip(dictionary["Rating"], dictionary["Hotel Name"]))]
            dictionary["Price Per Day"] = [x for _, x in sorted(zip(dictionary["Rating"], dictionary["Price Per Day"]))]
            dictionary["Address"] = [x for _, x in sorted(zip(dictionary["Rating"], dictionary["Address"]))]
            dictionary["Final Price"] = [x for _, x in sorted(zip(dictionary["Rating"], dictionary["Final Price"]))]
            dictionary["Link"] = [x for _, x in sorted(zip(dictionary["Rating"], dictionary["Link"]))]
            dictionary["Rating"] = sorted(dictionary["Rating"])
        case "highestperday":
            dictionary["Hotel Name"] = [x for _, x in
                                        sorted(zip(dictionary["Price Per Day"], dictionary["Hotel Name"]),
                                               reverse=True)]
            dictionary["Final Price"] = [x for _, x in
                                         sorted(zip(dictionary["Price Per Day"], dictionary["Final Price"]),
                                                reverse=True)]
            dictionary["Address"] = [x for _, x in
                                     sorted(zip(dictionary["Price Per Day"], dictionary["Address"]), reverse=True)]
            dictionary["Rating"] = [x for _, x in
                                    sorted(zip(dictionary["Price Per Day"], dictionary["Rating"]), reverse=True)]
            dictionary["Link"] = [x for _, x in
                                  sorted(zip(dictionary["Price Per Day"], dictionary["Link"]), reverse=True)]
            dictionary["Price Per Day"] = sorted(dictionary["Price Per Day"], reverse=True)
        case "highestfinal":
            dictionary["Hotel Name"] = [x for _, x in
                                        sorted(zip(dictionary["Final Price"], dictionary["Hotel Name"]), reverse=True)]
            dictionary["Price Per Day"] = [x for _, x in
                                           sorted(zip(dictionary["Final Price"], dictionary["Price Per Day"]),
                                                  reverse=True)]
            dictionary["Address"] = [x for _, x in
                                     sorted(zip(dictionary["Final Price"], dictionary["Address"]), reverse=True)]
            dictionary["Rating"] = [x for _, x in
                                    sorted(zip(dictionary["Final Price"], dictionary["Rating"]), reverse=True)]
            dictionary["Link"] = [x for _, x in
                                  sorted(zip(dictionary["Final Price"], dictionary["Link"]), reverse=True)]
            dictionary["Final Price"] = sorted(dictionary["Final Price"], reverse=True)
        case "highestrating":
            dictionary["Hotel Name"] = [x for _, x in
                                        sorted(zip(dictionary["Rating"], dictionary["Hotel Name"]), reverse=True)]
            dictionary["Price Per Day"] = [x for _, x in
                                           sorted(zip(dictionary["Rating"], dictionary["Price Per Day"]), reverse=True)]
            dictionary["Address"] = [x for _, x in
                                     sorted(zip(dictionary["Rating"], dictionary["Address"]), reverse=True)]
            dictionary["Final Price"] = [x for _, x in
                                         sorted(zip(dictionary["Rating"], dictionary["Final Price"]), reverse=True)]
            dictionary["Link"] = [x for _, x in
                                  sorted(zip(dictionary["Rating"], dictionary["Link"]), reverse=True)]
            dictionary["Rating"] = sorted(dictionary["Rating"], reverse=True)
    # Actually writing the csv file
    with open("hotels.csv", "w") as outfile:
        writer = csv.writer(outfile, delimiter=",")

        writer.writerow(dictionary.keys())
        writer.writerows(zip(*[dictionary[key] for key in dictionary.keys()]))


def get_city_name():
    """
    An error handler/getter to get city name from user input
    :return: a string of city input
    """
    while True:
        city_input = input("What city are you staying at?")

        if not city_input:
            print("You did not enter a city please enter a city")
        else:
            return city_input


def get_check_in_date():
    """
    Checks if the user input matches the YYYY/MM/DD format. Then checks if the date is earlier than current date.
    :return:  The string of user inputted check-in date
    """
    while True:
        check_in_input = input("Enter date to check in: Format = YYYY/MM/DD")

        # This checks if user input is actually the right format
        pattern_checker = re.compile(r'^\d{4}/\d{2}/\d{2}$')

        if pattern_checker.match(check_in_input):
            # This checks if this is actually a valid date
            date_inputted = datetime.strptime(check_in_input, "%Y/%m/%d").date()
            current_date = datetime.now().date()

            if date_inputted >= current_date:
                return check_in_input
            else:
                print("Please enter a valid check-in date.")
        else:
            print("Please enter a valid check-in date.")


def get_checkout_date(check_in_date):
    """
    Checks if the user input matches the YYYY/MM/DD format. Then checks if the date is earlier than check-in date.
    :param check_in_date: a YYYY/MM/DD string that represents check in date
    :return: a string in the right format for the checkout date
    """
    while True:
        check_out_input = input("Enter date to check out: Format = YYYY/MM/DD")

        # This checks if user input is actually the right format
        pattern_checker = re.compile(r'^\d{4}/\d{2}/\d{2}$')

        if pattern_checker.match(check_out_input):
            date_inputted = datetime.strptime(check_out_input, "%Y/%m/%d").date()
            date_to_compare = datetime.strptime(check_in_date, "%Y/%m/%d").date()

            if date_inputted > date_to_compare:
                return check_out_input
            else:
                print("Please enter a valid check-out date.")
        else:
            print("Please enter a valid check-out date.")


def get_travellers():
    """
    Asks the user for input for the amount of travellers, asks again if invalid
    :return: an int for number if travellers
    """
    while True:
        int_input = input("Number of travellers?")

        if not int_input:
            print("Please enter a number.")
        else:
            int_input = int(int_input)
            if int_input <= 0:
                print("Invalid number of travellers.")
            else:
                return int_input


def get_children():
    """
    Checks if the user actually typed something, asks again if they did not
    :return: int representing number of children
    """
    while True:
        int_input = input("Number of children?")

        if not int_input:
            print("Please enter a number.")
        else:
            int_input = int(int_input)
            return int_input


def get_children_age(no_of_children):
    """
    Asks the user for their children's age in AGE1/AGE2 format. Checks if it's in that format then checks if the number of ages
    inputted matches the number of children
    :param no_of_children: an int that represents the number of children
    :return: a string in AGE1/AGE2 format
    """
    while True:
        age_input = input("How old are your children?: Format = AGE1/AGE2")

        pattern_checker = re.compile(r'^\d{2}(/\d{2})*$')

        if pattern_checker.match(age_input):
            age_check = age_input.split("/")

            if no_of_children == len(age_check):
                return age_input
            else:
                print("Ages did not match number of children")
        else:
            print("Please enter in valid format")


def get_sort(choices):
    """
    Asks the user to input a str ing from (lowestperday, highestperday, lowestfinal, highestfinal, lowestrating, highestrating)
    checks if the input matches one of them
    :param choices: a list of string consisting of  (lowestperday, highestperday, lowestfinal, highestfinal, lowestrating, highestrating)
    :return: a string
    """
    sort_choice = ""
    while sort_choice not in choices:
        sort_choice = input("How would you like to sort the information?\n (lowestperday, highestperday, lowestfinal, "
                      "highestfinal, lowestrating, highestrating)")
    return sort_choice


def main():
    options = webdriver.ChromeOptions()

    options.add_argument(
        'user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/87.0.4280.141'
        'Mobile Safari/537.36')
    options.add_argument('accept-encoding=gzip, deflate, br')
    options.add_argument(
        'accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
        '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    options.add_argument('referer=https://www.expedia.ca/')
    options.add_argument('upgrade-insecure-requests=1')

    url = "https://www.expedia.ca/"
    # Ask user for specific data
    city_name = get_city_name()
    start_date = get_check_in_date()
    end_date = get_checkout_date(start_date)
    start_date = start_date.split("/")
    year_start = int(start_date[0])
    month_start = int(start_date[1])
    day_start = int(start_date[2])
    end_date = end_date.split("/")
    year_end = int(end_date[0])
    month_end = int(end_date[1])
    day_end = int(end_date[2])
    no_of_travellers = get_travellers()
    no_of_children = get_children()
    age_of_child = []
    if no_of_children > 0:
        age_of_child = get_children_age(no_of_children)
        age_of_child = age_of_child.split("/")
        age_of_child = list(map(int, age_of_child))
    sort_func = get_sort(["lowestperday", "highestperday", "lowestfinal","highestfinal", "lowestrating", "highestrating"])
    hotel_dict = webscrape(options, url, year_start, month_start, day_start, year_end, month_end, day_end, city_name,
                           no_of_travellers, no_of_children, age_of_child)
    output_to_csv(hotel_dict, sort_func)


if __name__ == '__main__':
    main()

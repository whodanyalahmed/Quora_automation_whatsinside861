from selenium import webdriver
import selenium
import sys
import time
import os
from sys import platform
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
# import first column of data from xlsx file
import pandas as pd
from os import link, listdir, getcwd
from os.path import isfile, join


def get_data_from_xlsx(file_name, sheet_name, column_name):
    data = pd.read_excel(file_name, sheet_name=sheet_name)
    # data = data[column_name]
    return data[column_name]


comments = get_data_from_xlsx('Quora.xlsx', 'Post Comments', 'Comments')
email = get_data_from_xlsx('Quora.xlsx', 'Accounts', 'Email')
password = get_data_from_xlsx('Quora.xlsx', 'Accounts', 'Password')
links = get_data_from_xlsx('Quora.xlsx', 'Post Link', 'Links')
print(comments)
print(links)


cur_path = sys.path[0]


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


if platform == "linux" or platform == "linux2":
    # linux
    path = resource_path('driver/chromedriver')
else:
    path = resource_path('i://clients/chromedriver.exe')


def Clicking_on(tag, text):
    driver.implicitly_wait(10)
    while True:
        try:
            xpath_for_OK_btn = "//*[contains(text(), '"+text+"')]"

            driver.find_element_by_xpath(
                '//'+tag+'[.'+xpath_for_OK_btn + ']').click()
            print('info: '+text+' button/text clicked')
            break
        except Exception as e:
            print("error: "+text+" button/text not found")
            print(e)
            continue
# chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--no-sandbox") # linux only
# chrome_options.headless = True # also works
# driver = webdriver.Chrome()
    # Windows...
# print("\n\nProcessing.....")


driver = webdriver.Chrome(path)
driver.maximize_window()


def go_Home():

    try:
        driver.get("https://quora.com")
        print('info: website loaded')
    except selenium.common.exceptions.TimeoutException:
        print("error: Page took too long to load")


go_Home()
# try filling email and password

# loop on emails
for i in range(len(email)):

    try:
        driver.find_element_by_id("email").send_keys("{}".format(email[i]))
        driver.find_element_by_id("password").send_keys(
            "{}".format(password[i]))
        print('info: email and password filled')
    except NoSuchElementException:
        print("error: email or password not found")


# try login
Clicking_on('button', 'Login')
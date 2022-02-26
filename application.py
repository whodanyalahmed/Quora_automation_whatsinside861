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


def chrome(headless=False):
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome(
        executable_path=r'i://clients//chromedriver.exe', options=opt, desired_capabilities=d)
    browser.implicitly_wait(10)
    browser.maximize_window()
    return browser


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


driver = chrome(headless=False)
driver.maximize_window()


def Click_on(tag, text):

    driver.implicitly_wait(10)
    try:
        xpath_for_OK_btn = "//*[contains(text(), '"+text+"')]"

        driver.find_element_by_xpath(
            '//'+tag+'[.'+xpath_for_OK_btn + ']').click()
        print('info: '+text+' button/text clicked')
    except Exception as e:
        print("error: "+text+" button/text not found")
        print(e)


def last_of_Click_on(text):
    # time.sleep(5)
    try:

        xpath_for_skip_import = "//span[@name='"+text+"']"
        skip_ele1 = driver.find_elements_by_xpath(
            "//button[."+xpath_for_skip_import+"]")
        # loop on skin_ele and get innerHTML
        # print("No. of close buttons: "+str(len(skip_ele1)))
        ele_item = skip_ele1[0]
        try:
            print("info: "+text+" button/text using try clicked")
            # ele_item.click()

            driver.execute_script("arguments[0].click();", ele_item)
        except:
            print("error: "+text+" button/text not found now using except")
            driver.execute_script("arguments[0].click();", ele_item)
        print('info: '+text+' button/text clicked')

    except Exception as e:
        print("error: "+text+" button/text not found")
        print(e)


def go_Home():

    try:
        driver.get("https://quora.com")
        print('info: website loaded')
    except selenium.common.exceptions.TimeoutException:
        print("error: Page took too long to load")


go_Home()
# try filling email and password

# loop on emails
driver.implicitly_wait(10)
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
    print("success: logged in")
    time.sleep(3)
    for l in range(len(links)):
        try:
            print(links[l])
            driver.get("{}".format(links[l]))
            print('info: link loaded')
        except selenium.common.exceptions.TimeoutException:
            print("error: Page took too long to load")

        # try to click on comment
        try:
            last_of_Click_on('Comment')
        except NoSuchElementException:
            print("error: comment button not found")

        # scroll 400px
        # driver.execute_script(
        #     "window.scrollTo(0, 500);")

        try:
            try:
                # wait for element to be visible
                # comment_add = WebDriverWait(driver, 10).until(
                #     EC.visibility_of_element_located((By.XPATH, 'div[@data-placeholder="Add a comment..."]')))
                time.sleep(5)
                print(comments[l])
                comment_add = driver.find_element_by_xpath(
                    '//div[@class="span"]')

                # get the div in comment_add with attribute data-kind="span"
                print(comment_add)
                print('info: comment box opened')
            except:
                print("error: comment box not found add a comment")
            comment_add.send_keys("{}".format(comments[l]))
            print('info: comment added')

            try:

                Click_on('button', 'Add Comment')

            except NoSuchElementException:
                print("error: Add comment button not found")
            time.sleep(5)
        except:
            print("cant type the commment")

        # try:
        #     print(comments[l])

        #     driver.find_element_by_xpath(

        #         'div[@data-placeholder="Add a comment..."]').send_keys(
        #         "{}".format(comments[l]))
        #     # press enter key
        #     driver.find_element_by_xpath(
        #         'div[@data-placeholder="Add a comment..."]').send_keys(
        #         Keys.ENTER)
        #     print('info: comment added')
        # except NoSuchElementException:
        #     print("error: comment not added")
# driver.quit()

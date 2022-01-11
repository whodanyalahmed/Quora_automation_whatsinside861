from selenium import webdriver
import selenium
import sys
import time
import os
from dotenv import load_dotenv
from sys import platform
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import first column of data from xlsx file
import pandas as pd


def get_data_from_xlsx(file_name, sheet_name, column_name):
    data = pd.read_excel(file_name, sheet_name=sheet_name)
    # data = data[column_name]
    return data[column_name]


questions = get_data_from_xlsx('data.xlsx', 'Question', 'Question')
answers = get_data_from_xlsx('data.xlsx', 'Question', 'Hyerlink')

cur_path = sys.path[0]
load_dotenv(dotenv_path='.env')


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


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# go to website and wait for it to load with try and except
try:
    driver.get("https://quora.com")
    print('info: website loaded')
except selenium.common.exceptions.TimeoutException:
    print("error: Page took too long to load")

# try filling email and password
email = os.environ['EMAIL']
password = os.environ['PASSWORD']

try:
    driver.find_element_by_id("email").send_keys("{}".format(email))
    driver.find_element_by_id("password").send_keys("{}".format(password))
    print('info: email and password filled')
except NoSuchElementException:
    print("error: email or password not found")


# try login
Clicking_on('button', 'Login')
# while True:
#     time.sleep(5)
#     try:
#         xpath_for_login_btn = "//*[contains(text(), 'Login')]"

#         driver.find_element_by_xpath(
#             '//button[.'+xpath_for_login_btn + ']').click()
#         print('info: login button clicked')
#         break
#     except Exception as e:
#         print("error: login button not found")
#         print(e)
#         continue
driver.implicitly_wait(10)
# time.sleep(5)
name_of_space = "Best riddles of 2003"
xpath_for_space_name = "//*[contains(text(), '"+name_of_space+"')]"
len_of_space_name = len(driver.find_elements_by_xpath(xpath_for_space_name))
if len_of_space_name > 0:
    print('info: space already exist')
    # space = driver.find_element_by_xpath(xpath_for_space_name)
    space = driver.find_element_by_xpath("//a[."+xpath_for_space_name + "]")
    # go to parent element anchor tag
    time.sleep(5)
    # anchor_tag = space.find_element_by_xpath('//ancestor::a[1]')
    # print(space.tag_name)
    # print(space.get_attribute('href'))
    space.click()
    print('info: space clicked')
    # close previous open tab
    driver.switch_to.window(driver.window_handles[0])
    # close current tab
    driver.close()
    # switch to new tab
    driver.switch_to.window(driver.window_handles[0])
    print('info: switched to new tab')
    # close tab 1

else:
    print('info: space not exist already creating one')
    # try creating a new space
    while True:

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//html/body/div[2]/div[2]/div[3]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]")))

            element.click()
            print('info: space created button clicked')
            break
        except Exception as e:
            print("error: space created button not found")
            print(e)
            continue
    # try naming the space
    try:
        textelement = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//html/body/div[2]/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/input")))
        driver.implicitly_wait(10)
        # clear the text in input box
        textelement.send_keys(Keys.CONTROL + 'a')
        textelement.send_keys(Keys.DELETE)
        print("info: input box cleared")
        textelement.send_keys(name_of_space)
        print('info: space name filled')
    except Exception as e:
        print("error: space name not found")
        print(e)
    # pressing create button
    try:
        driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/button").click()
        print('info: space created button clicked')

    except Exception as e:
        print("error: space created button not found")
        print(e)

    # # closing invite modal
    # while True:
    #     time.sleep(10)
    #     try:

    #         xpath_for_skip_importing = "//*[contains(text(), 'Skip importing')]"
    #         ele = driver.find_element_by_xpath(
    #             "//button[."+xpath_for_skip_importing+"]")

    #         # print(ele.tag_name)
    #         # print(ele.get_attribute('innerHTML'))
    #         ele.click()
    #         print('info: invite modal closed')
    #         break
    #     except Exception as e:
    #         print("error: invite modal not found")
    #         print(e)
        # continue
    while True:
        time.sleep(5)
        try:

            xpath_for_skip_import = "//span[@name='Close']"
            skip_ele1 = driver.find_elements_by_xpath(
                "//button[."+xpath_for_skip_import+"]")
            # loop on skin_ele and get innerHTML
            # print("No. of close buttons: "+str(len(skip_ele1)))
            ele_item = skip_ele1[-2]
            driver.execute_script("arguments[0].click();", ele_item)
            print('info: skip invite friends')
            break
        except Exception as e:
            print("error: skip invite friends not found")
            print(e)
            continue

            # clicking gear icon
# time.sleep(10)
# try:
#     setting_url = driver.current_url + "settings"
#     driver.get(setting_url)
#     print('info: gear icon clicked')
# except Exception as e:
#     print("error: gear icon not found")
#     print(e)
# time.sleep(5)
# scroll to 1000px
# while True:
#     driver.execute_script("window.scrollTo(0, 1000);")
#     # disabling post content type
#     try:
#         checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
#             # "//html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[6]/div[2]/div[3]/div/div[1]/label/div[3]"))
#             "//html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[6]/div[2]/div[3]/div/div[1]/label"))
#         # /html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[6]/div[2]/div[3]/div/div[1]/label
#         try:
#             checkbox.click()
#             print("info: using click")
#         except Exception as e:
#             print("info: using javascript")
#             driver.execute_script("arguments[0].click();", checkbox)

#         print('info: post content type disabled')
#         break
#     except Exception as e:
#         print("error: post content type not found")
#         print(e)
#         continue
# driver.back()
# print("info: back button clicked")

# clicking not now

Click_on('button', 'Not now')
Click_on('button', 'OK')


for question in len(questions):

    try:
        driver.find_element_by_xpath(
            "//*[contains(text(), 'Post in ')]").click()
        print('info: post in space clicked')
    except Exception as e:
        print("error: post in space not found")
        print(e)
    try:
        txt_input=driver.find_element_by_xpath(
            '//div[@data-placeholder="Say something..."]')
        print('info: text area clicked')
        txt_input.click()
        txt_input.send_keys(Keys.CONTROL + 'a')
        txt_input.send_keys(Keys.DELETE)
        txt_input.send_keys(questions[question])
    except Exception as e:
        print("error: text area not found")
        print(e)
    
    # print(questions[question])
    # print(answers[question])

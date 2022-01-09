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
while True:
    time.sleep(5)
    try:
        driver.find_element_by_xpath(
            '//html/body/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[5]/button').click()
        print('info: login button clicked')
        break
    except Exception as e:
        print("error: login button not found")
        print(e)
        continue
driver.implicitly_wait(10)
# time.sleep(5)
name_of_space = "Best riddles of 2020"
xpath_for_space_name = "//*[contains(text(), '"+name_of_space+"')]"
len_of_space_name = len(driver.find_elements_by_xpath(xpath_for_space_name))
if len_of_space_name > 0:
    print(len_of_space_name)
    print('info: space already exist')
    # space = driver.find_element_by_xpath(xpath_for_space_name)
    space = driver.find_element_by_xpath("//a[."+xpath_for_space_name + "]")
    # go to parent element anchor tag
    time.sleep(5)
    # anchor_tag = space.find_element_by_xpath('//ancestor::a[1]')
    print(space.tag_name)
    print(space.get_attribute('href'))
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
    print(len_of_space_name)
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

    # closing invite modal
    while True:
        time.sleep(10)
        try:
            ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                "//html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div[2]/button"))

            ele.click()
            print('info: invite modal closed')
            break
        except Exception as e:
            print("error: invite modal not found")
            print(e)
            continue
# clicking gear icon

try:
    setting_url = driver.current_url + "/settings"
    driver.get(setting_url)
    print('info: gear icon clicked')
except Exception as e:
    print("error: gear icon not found")
    print(e)

# scroll to 1000px
while True:
    driver.execute_script("window.scrollTo(0, 1000);")
    # disabling post content type
    try:
        checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            "//html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[6]/div[2]/div[3]/div/div[1]/label"))
        checkbox.click()
        print('info: post content type disabled')
        break
    except Exception as e:
        print("error: post content type not found")
        print(e)
        continue

driver.back()
print("info: back button clicked")

import json
import random
#from scheduler import Scheduler
#import scheduler.trigger as trigger
import schedule
import datetime
import time
from datetime import timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

chrome_options = Options()  # set chrome options
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1080,1920')

print("----> Launching Chrome")

driver = webdriver.Chrome(options=chrome_options)  # launch Chrome w/ options
print("----> Loading contest website")

driver.get("https://orvillecontest.ca/npn-entry")

print("----> Clicking form")
driver.find_element(By.XPATH, "/html/body/div/div/main/div/div/div/form/div[7]/button").click()  # submit form (eek):

time.sleep(5)
driver.save_screenshot(
    "tested " + str(datetime.datetime.now(timezone(timedelta(hours=-5.0)))) +
    ".png")
print("----> Clearing cache and quitting...")
driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
driver.execute_cdp_cmd("Network.clearBrowserCache", {})
driver.quit()
print("----> Finished with the browser!")

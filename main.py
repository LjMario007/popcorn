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

userDataPath = "userDataFile.json"  # Change this to your userdata file
essayFilePath = "sampleEssays.json"  # Change this to your essay file
logFilePath = "sampleLogFile.json"  # Change this to your log file
activatedMode = False  # Set to True to begin submissions!

def getEssayList(path):
    # return the dict
    with open(path) as essayFile:
        return json.load(essayFile)


def getLog(path):
    with open(path) as logFile:
        return json.load(logFile)


def getUserInfo(path):
    with open(path) as userInfo:
        return json.load(userInfo)

print("Loading user data from json files...")

userData = getUserInfo(userDataPath)  # returns dict with data
fullName = userData["fullName"]  # pull user info
email = userData["email"]
province = userData["province"]
essays = getEssayList(essayFilePath)
#ontarioTime = timezone(timedelta(hours=-5.0))
#schedule = Scheduler(tzinfo=ontarioTime)
random.seed(datetime.datetime.now().timestamp())

def submitContestEntry(name, email, province, essay):
    chrome_options = Options()  # set chrome options
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1080,1920')
  
    print("----> Launching Chrome")
  
    driver = webdriver.Chrome(options=chrome_options)  # launch Chrome w/ options
    print("----> Loading contest website")
  
    driver.get("https://orvillecontest.ca/npn-entry")

    print("----> Filling form")
  
    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "email").send_keys(email)
    dropdownBox = Select(driver.find_element(By.ID, "province"))
    dropdownBox.select_by_value(province)
    driver.find_element(By.ID, "message").send_keys(essay) # write essay
    for i in driver.find_elements(By.CLASS_NAME, "checkmark"):
        i.click()  # click ALL the checkboxes
    driver.save_screenshot("filled " + str(datetime.datetime.now(timezone(timedelta(hours=-5.0)))) + ".png")
    if activatedMode:
      driver.find_element(By.CLASS_NAME, "btn").click() # submit form (eek)
      print("----> FORM SUBMITTED FOR REALSIES!")
      sleep(3)
    else:
      print("----> FORM NOT ACTUALLY SUBMITTED, activatedMode = false")
    driver.save_screenshot("submitted " + str(datetime.datetime.now(timezone(timedelta(hours=-5.0)))) + ".png")
    print("----> Clearing cache and quitting...")
    driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
    driver.execute_cdp_cmd("Network.clearBrowserCache", {})
    driver.quit()
    print("----> Finished with the browser!")

def scheduledSubmission():
    # everday this is run
    # opens Log File
    print("Loading past submissions...")
    log = getLog(logFilePath)
    nextEssayIndex = len(log["submissions"]) - 1 # works cause will be one behind (0-indexed)
    lastSubmissionDate = log["submissions"][nextEssayIndex - 1]["dateTime"]
    nowTime = datetime.datetime.now(timezone(timedelta(hours=-5.0)))
  
    # runs submission
    if (lastSubmissionDate.split("/")[0] < nowTime.strftime("%d")) or (lastSubmissionDate.split("/")[1] != nowTime.strftime("%m")):
        # either the date is larger OR the month is not the same
        print("New day, submitting contest entry")
        submitContestEntry(fullName, email, province, essays[str(nextEssayIndex)])
        # Edits Log for last entry
        newestEntry = {
            "essayIndex":
            nextEssayIndex,
            "dateTime":
            nowTime.strftime("%d/%m/%Y"),
            "essaySubmitted":
            essays[str(nextEssayIndex)]
        }
        log["submissions"].append(newestEntry)

        with open(logFilePath, "w") as logFileToWrite:
            json.dump(log, logFileToWrite, indent=4)  # write to file
    else:
      print("Not submitting, already done today")

def delayedSubmission():
  sleepDelay = random.randint(1,28800)
  print("Delayed submission activated, waiting " + sleepDelay + " seconds (" + (sleepDelay / 3600) + ") hours")
  time.sleep(sleepDelay) # 8 hour range
  scheduledSubmission()

print("Checking if already submitted for today")
scheduledSubmission() # if program opened, run it immediately
print("Scheduling for a delayed submission at 9:02 am going forward")
schedule.every().day.at("09:02").do(delayedSubmission) # 24 hour time

while True:
    # Checks whether a scheduled task
    # is pending to run or not
  schedule.run_pending()
  time.sleep(1)
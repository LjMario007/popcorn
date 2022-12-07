import json
import random
from scheduler import Scheduler
import scheduler.trigger as trigger
import datetime
import time
from datetime import timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

userDataPath = "userDataFile.json" # Change this to your userdata file
essayFilePath = "leif1AIEssays.json" # Change this to your essay file
logFilePath = "newLogFile.json" # Change this to your log file
activatedMode = False # Set to True to begin submissions!

def getEssayList(path):
  # return the dict
  essayFile = open(path)
  return json.load(essayFile)

def getLog(path):
  logFile = open(path)
  return json.load(logFile)

def getUserInfo(path):
  userInfo = open(path)
  return json.load(userInfo)

def submitContestEntry(name, email, province, essay):
  chrome_options = Options() # set chrome options
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--window-size=1080,1920')

  driver = webdriver.Chrome(options=chrome_options) # launch Chrome w/ options
  driver.get("https://orvillecontest.ca/npn-entry")
  
  driver.find_element(By.ID, "name").send_keys(name)
  driver.find_element(By.ID, "email").send_keys(email)
  dropdownBox = Select(driver.find_element(By.ID, "province"))
  dropdownBox.select_by_value(province)
  driver.find_element(By.ID, "message").send_keys(essay)
  for i in driver.find_elements(By.CLASS_NAME, "checkmark"):
    i.click() # click ALL the checkboxes
  if activatedMode:
    driver.find_element(By.CLASS_NAME, "btn").click()
  driver.save_screenshot(str(datetime.datetime.now(timezone(timedelta(hours=-5.0)))) + ".png")
  driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
  driver.execute_cdp_cmd("Network.clearBrowserCache", {})
  driver.quit()


userData = getUserInfo(userDataPath) # returns dict with data
fullName = userData["fullName"] # pull user info
email = userData["email"]
province = userData["province"]
essays = getEssayList(essayFilePath)
ontarioTime = timezone(timedelta(hours=-5.0))
schedule = Scheduler(tzinfo=ontarioTime)
random.seed(datetime.datetime.now().timestamp())

def scheduledSubmission():
  # everday this is run
  # opens Log File
  log = getLog(logFilePath)
  nextEssayIndex = len(log["submissions"])
  lastSubmissionDate = log["submissions"][nextEssayIndex-1]["date"]
  
  # runs submission
  if (lastSubmissionDate.split("/")[0] < datetime.datetime.now(timezone(timedelta(hours=-5.0))).strftime("%d")) or (lastSubmissionDate.split("/")[1] != timezone(timedelta(hours=-5.0)).strftime("%m")):
    submitContestEntry(fullName, email, province, essays[str(nextEssayIndex)])
    # Edits Log for last entry
    newestEntry = {"index": nextEssayIndex, "date": datetime.datetime.now(timezone(timedelta(hours=-5.0))).strftime("%d/%m/%Y"), "essaySubmitted": essays[str(nextEssayIndex)]}
    log["submissions"].append(newestEntry)
    
  tomorrow = datetime.datetime.now(timezone(timedelta(hours=-5.0))) + timedelta(day=1)
  nextHour = random.randint(9,6)
  nextMinute = random.randint(0,59)
  
  schedule.once(dt.datetime(year=tomorrow.strftime("%y"), month=tomorrow.strftime("%m"), day=tomorrow.strftime("%d"), hour = nextHour, minute=nextMinute), scheduledSubmission)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.exec_jobs()
    time.sleep(1)

#scheduledSubmission()


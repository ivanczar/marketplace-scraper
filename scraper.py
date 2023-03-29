import os
from dotenv import load_dotenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import keywords
import pywhatkit


load_dotenv()
URL = os.getenv("URL")
email = os.getenv("EMAIL")
password = os.getenv("PSWD")
phone = os.getenv("TO_PHONE")
keywords = keywords.words
match = ""
freeCount = 0
matchCount = 0

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# # login
driver.get(URL)
driver.find_element(By.ID, "username").send_keys(email)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, "//div[@class='password-submit']/button").click()

sleep(5)
# nav to markeplace
driver.find_element(By.LINK_TEXT, "Market").click()
sleep(5)

# get all listings
allListings = driver.find_elements(By.CLASS_NAME, "market-item")
for listing in allListings:
    title = listing.find_element(
        By.CLASS_NAME, "market-item-subject").text
    price = listing.find_element(
        By.CLASS_NAME, "lozenge").text
    if "Free" in price:
        freeCount += 1
    for item in keywords:
        if item in title.lower():
            match += f"\t-{title}\n"
            matchCount += 1

# Only create message object if matchCount != 0 (prevent empty messages)
pywhatkit.sendwhatmsg_instantly(phone, (
    f'● Found {freeCount} free items \n● Found {matchCount} items matching criteria: {match}'))

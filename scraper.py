# import os
# from dotenv import load_dotenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import keywords


# load_dotenv()
# URL = os.getenv("URL")
# email = os.getenv("EMAIL")
# password = os.getenv("PSWD")
# phone = os.getenv("TO_PHONE")
keywords = keywords.words
match = ""
freeCount = 0
matchCount = 0

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # login
print("Logging in...")
driver.get('https://www.neighbourly.co.nz/login')
driver.find_element(By.ID, "username").send_keys('ivanczar2013@gmail.com')
driver.find_element(By.ID, "password").send_keys('kukilin1')
driver.find_element(By.XPATH, "//div[@class='password-submit']/button").click()
print("Logged in!")

sleep(5)
# nav to markeplace
print("Navigating to marketplace...")
driver.find_element(By.LINK_TEXT, "Market").click()
sleep(5)

# get all listings
print("Scraping listings...")
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
print(f'● Found {freeCount} free items \n● Found {matchCount} items matching criteria: {match}')
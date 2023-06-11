import os
from dotenv import load_dotenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import keywords
import yagmail
from utils import pluralize


load_dotenv()
URL = os.getenv("URL")
TO_EMAIL = os.getenv("TO_EMAIL")
TO_PSWD = os.getenv("TO_PSWD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_PSWD = os.getenv("FROM_PSWD")


# set up driver
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)


keywords = keywords.words
match = ""
matchCount = 0

f = open("last_listing.txt", "r")
lastScrapedTitle = f.read()


# login
print("Logging in...")
driver.get(URL)
driver.find_element(By.ID, "username").send_keys(TO_EMAIL)
driver.find_element(By.ID, "password").send_keys(TO_PSWD)
driver.find_element(By.XPATH, "//div[@class='password-submit']/button").click()
print("Logged in!")
sleep(5)


# nav to markeplace
print("Navigating to marketplace...")
driver.find_element(By.LINK_TEXT, "Market").click()
sleep(5)


# get all listings
print("Scraping listings...")
listingsArr = driver.find_elements(By.CLASS_NAME, "market-item")
firstListingTitle = listingsArr[0].find_element(By.CLASS_NAME, "market-item-subject").text
    
for listing in listingsArr:
    title = listing.find_element(
        By.CLASS_NAME, "market-item-subject").text
    price = listing.find_element(
        By.CLASS_NAME, "lozenge").text
    
    if (title != lastScrapedTitle): # if not last scraped listing
        for item in keywords:
            if (item or pluralize(item)) in title.lower():
                match += f"\t-{title}\n"
                matchCount += 1
    else:
        break


f = open("last_listing.txt", "w")
f.write(firstListingTitle)


# send email
if (matchCount != 0):
    yag = yagmail.SMTP(FROM_EMAIL, FROM_PSWD)
    contents = [f'● Found {matchCount} items matching criteria: {match}']
    yag.send(TO_EMAIL, f'Neighbourly Scrape ({matchCount} matches)', contents)
    print("Email sent!")


f.close()
driver.close()


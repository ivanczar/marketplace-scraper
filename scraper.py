from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
load_dotenv()


URL = os.getenv("URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PSWD")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# login
driver.get(URL)
driver.find_element(By.ID, "username").send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//div[@class='password-submit']/button").click()
sleep(5)

# nav to markeplace
driver.find_element(By.LINK_TEXT, "Market").click()
sleep(5)

# get all listings
allListings = driver.find_elements(By.CLASS_NAME, "market-item")
for listing in allListings:
    listingTitle = listing.find_element(
        By.CLASS_NAME, "market-item-subject").text
    print(listingTitle)

sleep(100000)

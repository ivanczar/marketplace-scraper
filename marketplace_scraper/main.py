import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from time import sleep
from marketplace_scraper.web_driver import Driver
from marketplace_scraper.scraper import Scraper
from marketplace_scraper.email_driver import Email


load_dotenv()
URL = os.getenv("URL") or ""
TO_EMAIL = os.getenv("TO_EMAIL") or ""
TO_PSWD = os.getenv("TO_PSWD") or ""
FROM_EMAIL = os.getenv("FROM_EMAIL") or ""
FROM_PSWD = os.getenv("FROM_PSWD") or ""

webdriver = Driver().driver
webscraper = Scraper(webdriver)
emailClient = Email(FROM_EMAIL, FROM_PSWD)

webscraper.login(URL, TO_EMAIL, TO_PSWD)
sleep(5)
webscraper.navToMarketplace()
sleep(5)
listings = webscraper.scrapeListings()

if listings.count:
    emailClient.send(listings, TO_EMAIL)
else:
    print("No new listings found")

webdriver.quit()

# marketplace_scraper/__init__.py

import os
from dotenv import load_dotenv
from marketplace_scraper.web_driver import Driver
from marketplace_scraper.scraper import Scraper
from marketplace_scraper.email_driver import Email

def run_scraper():
    load_dotenv()

    LOGIN_URL = os.getenv("LOGIN_URL") or ""
    AUTHENTICATED_URL = os.getenv("AUTHENTICATED_URL") or ""
    TO_EMAIL = os.getenv("TO_EMAIL") or ""
    TO_PSWD = os.getenv("TO_PSWD") or ""
    FROM_EMAIL = os.getenv("FROM_EMAIL") or ""
    FROM_PSWD = os.getenv("FROM_PSWD") or ""

    webdriver = Driver().driver
    webscraper = Scraper(webdriver)
    emailClient = Email(FROM_EMAIL, FROM_PSWD)

    listings = webscraper.scrape(LOGIN_URL, AUTHENTICATED_URL, TO_EMAIL, TO_PSWD)

    if listings.getListingCount():
        emailClient.send(listings, TO_EMAIL)
        yield "data: Email sent!\n\n"
    else:
        print("No new listings found")
        yield "data: No new listings found\n\n"

    webdriver.quit()

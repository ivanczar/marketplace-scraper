import os
from dotenv import load_dotenv
from marketplace_scraper.web_driver import Driver
from marketplace_scraper.scraper import Scraper
from marketplace_scraper.email_driver import Email

def run_scraper():
    load_dotenv()

    login_url = os.getenv("LOGIN_URL") or ""
    authenticated_url = os.getenv("AUTHENTICATED_URL") or ""
    to_email = os.getenv("TO_EMAIL") or ""
    to_pswd = os.getenv("TO_PSWD") or ""
    from_email = os.getenv("FROM_EMAIL") or ""
    from_pswd = os.getenv("FROM_PSWD") or ""

    webdriver = Driver().driver
    webscraper = Scraper(webdriver)
    email_client = Email(from_email, from_pswd)

    listings = webscraper.scrape(login_url, authenticated_url, to_email, to_pswd)

    if listings.get_listing_count():
        email_client.send(listings, to_email)
        yield "data: Email sent!\n\n"
    else:
        print("No new listings found")
        yield "data: No new listings found\n\n"

    webdriver.quit()

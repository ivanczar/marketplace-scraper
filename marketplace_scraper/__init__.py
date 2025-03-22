import os
from dotenv import load_dotenv
from marketplace_scraper.web_driver import Driver
from marketplace_scraper.scraper import Scraper
from marketplace_scraper.email_driver import Email
from marketplace_scraper.discord_driver import Discord

def run_scraper():
    load_dotenv()

    login_url = os.getenv("LOGIN_URL") or ""
    authenticated_url = os.getenv("AUTHENTICATED_URL") or ""
    to_email = os.getenv("TO_EMAIL") or ""
    to_pswd = os.getenv("TO_PSWD") or ""
    from_email = os.getenv("FROM_EMAIL") or ""
    from_pswd = os.getenv("FROM_PSWD") or ""
    discord_webhook = os.getenv("DISCORD_WEBHOOK") or ""


    webdriver = Driver().driver
    webscraper = Scraper(webdriver)
    email_client = Email(from_email, from_pswd)
    discord_client = Discord(discord_webhook)

    try:
        yield "data: scraping_started\n\n"
        listings = webscraper.scrape(login_url, authenticated_url, to_email, to_pswd)

        if listings.get_listing_count():
            email_client.send(listings, to_email)
            discord_client.send(listings)
            yield "data: scraping_complete\n\n"
        else:
            print("No new listings found")
            yield "data: scraping_complete\n\n"

    except Exception as e:
        yield f"data: scraping_error: {str(e)}\n\n"
    finally:
        webdriver.stop_client()
        webdriver.close()
        webdriver.quit()

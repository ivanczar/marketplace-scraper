import os
from dotenv import load_dotenv
from time import sleep
import driver;
import scraper;
import email;

# rename env variables

load_dotenv()
URL = os.getenv("URL")
TO_EMAIL = os.getenv("TO_EMAIL")
TO_PSWD = os.getenv("TO_PSWD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_PSWD = os.getenv("FROM_PSWD")

webdriver = driver();
webscraper = scraper(webdriver);
emailClient = email(FROM_EMAIL, FROM_PSWD);

webscraper.login(URL, TO_EMAIL, TO_PSWD);
sleep(5)
webscraper.navToMarketplace();
sleep(5)
data = webscraper.searchAllListings();

if (data.totalMatchCount != 0):
    emailClient.send(data, TO_EMAIL)
else:
    print("No new listings found")

webdriver.close()

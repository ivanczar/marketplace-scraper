from selenium.webdriver.common.by import By
from config import keywords
from marketplace_scraper.utils import (
    pluralize,
    getLastScrapedTitle,
    setLastScrapedTitle,
)
from marketplace_scraper.matched_listings import MatchedListings
from selenium.webdriver.chrome.webdriver import WebDriver
import os


class Scraper:
    LAST_LISTING_FILE_PATH = os.path.join(
        os.path.dirname(__file__), "..", "data", "last_listing.txt"
    )
    KEYWORDS = keywords.words

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.lastScrapedTitle = getLastScrapedTitle(self.LAST_LISTING_FILE_PATH)
        self.result = MatchedListings()

    def login(self, url: str, email: str, pswd: str) -> None:
        print("Logging in...")
        self.driver.get(url)
        self.driver.find_element(By.ID, "username").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(pswd)
        self.driver.find_element(
            By.XPATH, "//div[@class='password-submit']/button"
        ).click()
        print("Logged in!")

    def navToMarketplace(self):
        print("Navigating to marketplace...")
        self.driver.find_element(By.LINK_TEXT, "Market").click()

    def getListings(self):
        return self.driver.find_elements(By.CLASS_NAME, "market-item")

    def scrapeListings(self) -> MatchedListings:
        print("Scraping listings...")
        listings = self.getListings()
        firstListingTitle = (
            listings[0].find_element(By.CLASS_NAME, "market-item-subject").text
        )

        for listing in listings:
            listingTitle = listing.find_element(
                By.CLASS_NAME, "market-item-subject"
            ).text
            listingPrice = listing.find_element(By.CLASS_NAME, "lozenge").text
            listingImage = listing.find_element(
                By.CSS_SELECTOR, ".image img"
            ).get_attribute("src")

            if listingTitle != self.lastScrapedTitle:  # if not last scraped listing
                for keyword in self.KEYWORDS:
                    if (keyword or pluralize(keyword)) in listingTitle.lower():
                        self.result.addListing(listingTitle, listingPrice, listingImage)
            else:
                break

        setLastScrapedTitle(self.LAST_LISTING_FILE_PATH, firstListingTitle)

        return self.result

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
from time import sleep


class Scraper:
    LAST_LISTING_FILE_PATH = os.path.join(
        os.path.dirname(__file__), "..", "data", "last_listing.txt"
    )
    KEYWORDS = keywords.words

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.lastScrapedTitle = getLastScrapedTitle(self.LAST_LISTING_FILE_PATH)
        self.matchingListings = MatchedListings()

    def scrape(self, url: str, email: str, pswd: str) -> MatchedListings:
        self.login(url,email,pswd)
        sleep(5)
        self.navToMarketplace()
        sleep(5)
        return self.getMatchingListings()

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

    def getAllListings(self):
        return self.driver.find_elements(By.CLASS_NAME, "market-item")

    def getMatchingListings(self) -> MatchedListings:
        print("Scraping listings...")
        listings = self.getAllListings()

        firstListingTitle = listings[0].find_element(By.CLASS_NAME, "market-item-subject").text

        for listing in listings:
            titleElement = listing.find_element(By.CLASS_NAME, "market-item-subject")
            listingTitle = titleElement.text
            listingTitleLower = listingTitle.lower()
            
            # Check to prevent scraping duplicates
            if listingTitle == self.lastScrapedTitle:
                break

            priceElement = listing.find_element(By.CLASS_NAME, "lozenge")
            imageElement = listing.find_element(By.CSS_SELECTOR, ".image img")
            
            listingPrice = priceElement.text
            listingImage = imageElement.get_attribute("src")

            # Get titles containing keywords
            if any(
                keyword in listingTitleLower or pluralize(keyword) in listingTitleLower
                for keyword in self.KEYWORDS
            ):
                self.matchingListings.addListing(listingTitle, listingPrice, listingImage)

            setLastScrapedTitle(self.LAST_LISTING_FILE_PATH, firstListingTitle)

            return self.matchingListings

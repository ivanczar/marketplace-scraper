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
import pickle
import os


class Scraper:
    LAST_LISTING_FILE_PATH = os.path.join(
        os.path.dirname(__file__), "..", "data", "last_listing.txt"
    )
    COOKIES_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "cookies.pkl"
    )
    KEYWORDS = keywords.words
    PRICE_FREE = "Free"
    PRICE_NEGOTIABLE = "Negotiable"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.lastScrapedTitle = getLastScrapedTitle(self.LAST_LISTING_FILE_PATH)
        self.matchingListings = MatchedListings()

    def scrape(self, loginUrl: str, authenticatedUrl: str, email: str, pswd: str) -> MatchedListings:
        self.login(loginUrl, authenticatedUrl, email, pswd)
        sleep(5)
        self.navToMarketplace()
        sleep(5)
        return self.getMatchingListings()
    
    def isLoggedIn(self):
        element = self.driver.find_element(By.XPATH, '/html/body/header/nav/div/div[2]/ul/li[1]/a') # only visible when authenticated
        return bool(element)

    def login(self, loginUrl: str, authenticatedUrl: str, email: str, pswd: str) -> None:
        print("Logging in...")
        self.driver.get(loginUrl)
        sleep(5)
        
       # Load cookies if available
        if os.path.exists(self.COOKIES_FILE_PATH) and os.path.getsize(self.COOKIES_FILE_PATH) > 0:
            print('Loading cookies...')
            try:
                with open(self.COOKIES_FILE_PATH, "rb") as file:
                    cookies = pickle.load(file)
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
                print("Cookies loaded successfully!")

                self.driver.get(authenticatedUrl)
                sleep(3)
                if self.isLoggedIn():
                    print("Logged in using cookies!")
                    return
            except (FileNotFoundError, pickle.UnpicklingError) as e:
                print(f"Error loading cookies: {e}")

        # Manual login if cookies fail or are not present
        print("Using username and password...")
        self.driver.find_element(By.ID, "username").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(pswd)
        self.driver.find_element(By.XPATH, "//div[@class='password-submit']/button").click()
        sleep(5)

        # Save cookies only if successfully logged in
        if self.isLoggedIn:
            print("Saving cookies...")
            with open(self.COOKIES_FILE_PATH, "wb") as file:
                pickle.dump(self.driver.get_cookies(), file)
            print("Cookies saved successfully!")
        else:
            print("Login failed.")

    def navToMarketplace(self):
        print("Navigating to marketplace...")
        self.driver.find_element(By.LINK_TEXT, "Market").click()

    def getAllListings(self):
        return self.driver.find_elements(By.CLASS_NAME, "market-item")

    def getMatchingListings(self) -> MatchedListings:
        print("Scraping listings...")
        listings = self.getAllListings()

        firstListingTitle = (
            listings[0].find_element(By.CLASS_NAME, "market-item-subject").text
        )

        for listing in listings:
            titleElement = listing.find_element(By.CLASS_NAME, "market-item-subject")
            listingTitle = titleElement.text

            # Check to prevent scraping duplicates
            if listingTitle == self.lastScrapedTitle:
                break

            priceElement = listing.find_element(By.CLASS_NAME, "lozenge")
            imageElement = listing.find_element(By.CSS_SELECTOR, ".image img")

            listingPrice = self.getFormattedPrice(priceElement.text)
            listingImage = imageElement.get_attribute("src")

            # Get titles containing keywords
            if self.isMatchingListing(listingTitle, listingPrice):
                self.matchingListings.addListing(
                    listingTitle, listingPrice, listingImage
                )

        setLastScrapedTitle(self.LAST_LISTING_FILE_PATH, firstListingTitle)

        return self.matchingListings

    def isMatchingListing(self, title: str, price: int) -> bool:
        titleLower = title.lower()

        for keyword, maxPrice in self.KEYWORDS.items():
            isKeywordInTitle = keyword in titleLower or pluralize(keyword) in titleLower

            if isKeywordInTitle and (maxPrice == None or price <= maxPrice):
                return True

        return False

    def getFormattedPrice(self, price: str) -> int:
        match price:
            case self.PRICE_NEGOTIABLE:
                return 0
            case self.PRICE_FREE:
                return 0
            case _:
                floatPrice = float(price.replace("$", "").replace(",", ""))
                return int(floatPrice)

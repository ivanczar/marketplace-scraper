import os
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from config import keywords
from marketplace_scraper.utils import (
    pluralize,
    get_last_scraped_title,
    set_last_scraped_title,
)
from marketplace_scraper.matched_listings import MatchedListings


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
    ACCOUNT_DROPDOWN_XPATH='/html/body/header/nav/div/div[2]/ul/li[1]/a'

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.last_scraped_title = get_last_scraped_title(self.LAST_LISTING_FILE_PATH)
        self.matching_listings = MatchedListings()

    def scrape(
        self, login_url: str,
        authenticated_url: str,
        email: str,
        pswd: str) -> MatchedListings:
        self.login(login_url, authenticated_url, email, pswd)
        self.nav_to_marketplace()
        return self.get_matching_listings()

    def is_logged_in(self):
        try:
            element = self.driver.find_element(By.XPATH, self.ACCOUNT_DROPDOWN_XPATH)
            return bool(element)
        except NoSuchElementException:
            print("User is not logged in.")
            return False

    def login(self, login_url: str, authenticated_url: str, email: str, pswd: str) -> None:
        print("Logging in...")
        self.driver.get(login_url)
       # Load cookies if available
        if os.path.exists(self.COOKIES_FILE_PATH) and os.path.getsize(self.COOKIES_FILE_PATH) > 0:
            print('Loading cookies...')
            try:
                with open(self.COOKIES_FILE_PATH, "rb") as file:
                    cookies = pickle.load(file)
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
                print("Cookies loaded successfully!")
                self.driver.refresh() # Needed to apply cookies
                self.driver.get(authenticated_url)

                if self.is_logged_in():
                    print("Logged in using cookies!")
                    return
            except (FileNotFoundError, pickle.UnpicklingError) as e:
                print(f"Error loading cookies: {e}")

        # Manual login if cookies fail or are not present
        print("Using username and password...")
        self.driver.find_element(By.ID, "username").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(pswd)
        self.driver.find_element(By.XPATH, "//div[@class='password-submit']/button").click()

        # Save cookies only if successfully logged in
        if self.is_logged_in():
            print("Saving cookies...")
            with open(self.COOKIES_FILE_PATH, "wb") as file:
                pickle.dump(self.driver.get_cookies(), file)
            print("Cookies saved successfully!")
        else:
            print("Login failed.")

    def nav_to_marketplace(self):
        print("Navigating to marketplace...")
        self.driver.find_element(By.LINK_TEXT, "Market").click()

    def get_all_listings(self):
        return self.driver.find_elements(By.CLASS_NAME, "market-item")

    def get_matching_listings(self) -> MatchedListings:
        print("Scraping listings...")
        listings = self.get_all_listings()

        first_listing_title = (
            listings[0].find_element(By.CLASS_NAME, "market-item-subject").text
        )

        for listing in listings:
            title_element = listing.find_element(By.CLASS_NAME, "market-item-subject")
            listing_title = title_element.text

            # Check to prevent scraping duplicates
            if listing_title == self.last_scraped_title:
                break

            price_element = listing.find_element(By.CLASS_NAME, "lozenge")
            image_element = listing.find_element(By.CSS_SELECTOR, ".image img")

            listing_price = self.get_formatted_price(price_element.text)
            listing_image = image_element.get_attribute("src")

            # Get titles containing keywords
            if self.is_matching_listing(listing_title, listing_price):
                self.matching_listings.add_listing(
                    listing_title, listing_price, listing_image
                )

        set_last_scraped_title(self.LAST_LISTING_FILE_PATH, first_listing_title)

        return self.matching_listings

    def is_matching_listing(self, title: str, price: int) -> bool:
        title_lower = title.lower()

        for keyword, max_price in self.KEYWORDS.items():
            is_keyword_in_title = keyword in title_lower or pluralize(keyword) in title_lower

            if is_keyword_in_title and (max_price is None or price <= max_price):
                return True

        return False

    def get_formatted_price(self, price: str) -> int:
        match price:
            case self.PRICE_NEGOTIABLE:
                return 0
            case self.PRICE_FREE:
                return 0
            case _:
                float_price = float(price.replace("$", "").replace(",", ""))
                return int(float_price)

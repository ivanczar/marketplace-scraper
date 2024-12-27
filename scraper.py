from selenium.webdriver.common.by import By
import keywords
from utils import pluralize, getLastScrapedTitle, setLastScrapedTitle


class Scraper:
    LAST_LISTING_FILE_PATH = "last_listing.txt"
    KEYWORDS = keywords.words

    def __init__(self, driver):
        self.driver = driver
        self.lastScrapedTitle = getLastScrapedTitle(
            self.LAST_LISTING_FILE_PATH)
        self.result = self.MatchedListings()

    def login(self, url, email, pswd):
        print("Logging in...")
        self.driver.get(url)
        self.driver.find_element(By.ID, "username").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(pswd)
        self.driver.find_element(
            By.XPATH, "//div[@class='password-submit']/button").click()
        print("Logged in!")

    def navToMarketplace(self):
        print("Navigating to marketplace...")
        self.driver.find_element(By.LINK_TEXT, "Market").click()

    def getListings(self):
        print("Getting listings...")
        return self.driver.find_elements(By.CLASS_NAME, "market-item")

    def scrapeListings(self):
        print("Scraping listings...")
        listings = self.getListings()
        firstListingTitle = listings[0].find_element(
            By.CLASS_NAME, "market-item-subject").text

        for listing in listings:
            listingTitle = listing.find_element(
                By.CLASS_NAME, "market-item-subject").text
            listingPrice = listing.find_element(
                By.CLASS_NAME, "lozenge").text

            if (listingTitle != self.lastScrapedTitle):  # if not last scraped listing
                for keyword in self.KEYWORDS:
                    if (keyword or pluralize(keyword)) in listingTitle.lower():
                        self.result.titles.append(
                            f"\t-{listingTitle}: {listingPrice}\n")
                        self.result.count += 1
            else:
                break

        setLastScrapedTitle(self.LAST_LISTING_FILE_PATH, firstListingTitle)

        return self.result

    class MatchedListings:
        def __init__(self):
            self.count = 0
            self.titles = []
            self.prices = []

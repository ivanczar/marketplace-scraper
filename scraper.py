from selenium.webdriver.common.by import By
import keywords
from utils import pluralize, getLastScrapedTitle, setLastScrapedTitle

class Scraper:
    LAST_LISTING_FILE_PATH = "last_listing.txt";

    def __init__(self, driver):
        self.driver = driver;
        self.keywords = keywords.words;
        self.lastScrapedTitle = getLastScrapedTitle(self.LAST_LISTING_FILE_PATH)
        self.result = self.MatchingListings();

    def login(self, url, email, pswd):
        print("Logging in...")
        self.driver.get(url)
        self.driver.find_element(By.ID, "username").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(pswd)
        self.driver.find_element(By.XPATH, "//div[@class='password-submit']/button").click()
        print("Logged in!")

    def navToMarketplace(self):
        print("Navigating to marketplace...")
        self.driver.find_element(By.LINK_TEXT, "Market").click()

    def getAllListings(self):
        print("Scraping listings...")
        return self.driver.find_elements(By.CLASS_NAME, "market-item")
        
    def searchAllListings(self):
        allListings = self.getAllListings();
        firstListingTitle = allListings[0].find_element(By.CLASS_NAME, "market-item-subject").text

        for listing in allListings:
            listingTitle = listing.find_element(
                By.CLASS_NAME, "market-item-subject").text
            listingPrice = listing.find_element(
                By.CLASS_NAME, "lozenge").text
            
            if (listingTitle != self.lastScrapedTitle): # if not last scraped listing
                for keyword in keywords:
                    if (keyword or pluralize(keyword)) in listingTitle.lower():
                        self.result.listingsTitles += f"\t-{listingTitle}: {listingPrice}\n"
                        self.result.totalMatchCount += 1;
            else:
                break

        setLastScrapedTitle(self.LAST_LISTING_FILE_PATH, firstListingTitle);

    class MatchingListings:
        def __init__(self):
            self.totalMatchCount = 0;
            self.listingsTitles = "\n";
            self.listingPrices = [];

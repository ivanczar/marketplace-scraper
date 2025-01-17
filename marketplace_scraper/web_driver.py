from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class Driver:
    CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

    def __init__(self, options=None):
        self.driver = self.setupDriver(options)

    def setupDriver(self, options=None) -> WebDriver:
        print("Initializing web driver...")
        if options is None:
            print("Using default driver options.")
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-gpu")

        chromeService = Service(self.CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=chromeService, options=options)
        driver.implicitly_wait(120)

        return driver

    def quit(self) -> None:
        self.driver.quit()

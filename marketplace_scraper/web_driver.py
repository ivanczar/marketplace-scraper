from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class Driver:
    CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

    def __init__(self, options=None):
        self.driver = self.setup_driver(options)

    def setup_driver(self, options=None) -> WebDriver:
        print("Initializing web driver...")
        if options is None:
            print("Using default driver options.")
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")  # Set window size
            options.add_argument("--disable-crash-reporter")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-in-process-stack-traces")
            options.add_argument("--disable-logging")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-setuid-sandbox")
            options.add_argument("--log-level=3")  # Suppress logs
            options.add_argument("--remote-debugging-port=9222")  # Avoid conflicts

        chrome_service = Service(self.CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.implicitly_wait(20)

        return driver

    def quit(self) -> None:
        self.driver.quit()

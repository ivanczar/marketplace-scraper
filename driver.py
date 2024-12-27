from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class Driver:

    def __init__(self, options):
        options = Options();
        options.add_argument('--headless');
        options.add_argument('--no-sandbox');
        options.add_argument('--disable-dev-shm-usage');
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options);

    def close(self):
        self.driver.close();

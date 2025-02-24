# config/selenium_scraper.py
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import datetime
from dotenv import load_dotenv
import os


class SeleniumScraper(ABC):
    """ Selenium-based web scraper with configurable settings. """
    load_dotenv()

    def __init__(self, headless=False, wait_time=5, use_fake_agent=True):
        super().__init__()
        self.config_option(headless, use_fake_agent)
        self.setup_driver(wait_time)
        self.set_constants()
        pass

    def set_constants(self):
        print(f"START_SEASON: {os.getenv('START_SEASON')}")
        self.SAVE_PATH = os.getenv("SAVE_PATH")
        self.START_SEASON = int(os.getenv("START_SEASON"))
        self.current_season = self.get_current_season()
        print(f"📌 start season {self.START_SEASON}")
        print(f"📌 current season {self.current_season}")
        pass

    def config_option(self, headless, use_fake_agent):
        """Configure options for the WebDriver."""
        self.options = Options()
        if headless:
            self.options.add_argument("--headless=new")
        # Random User-Agent
        if use_fake_agent:
            self.options.add_argument(f"user-agent={UserAgent().random}")
        # Anti-bot measures
        self.options.add_argument(
            "--disable-blink-features=AutomationControlled")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        pass

    def setup_driver(self, wait_time):
        """ Initialize WebDriver with options. """

        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.options)
        self.wait_time = wait_time

    def get_current_season(self):
        """ Determine the current football season. """
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        return current_year - 1 if current_month <= 6 else current_year

    def get(self, url):
        """ Open URL and wait. """
        self.driver.get(url)
        # time.sleep(random.uniform(self.wait_time, self.wait_time + 2))

    def find_element(self, by, value):
        """ Find a single element. """
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        """ Find multiple elements. """
        return self.driver.find_elements(by, value)

    def quit(self):
        """ Close the WebDriver. """
        self.driver.quit()

    @abstractmethod
    def scrape_data(self, season):
        """ Abstract method to scrape data for a given season. """
        pass

    @abstractmethod
    def save_data(self, dataframe, season):
        """ Abstract method to save scraped data. """
        pass

    @abstractmethod
    def get_old_seasons_data(self):
        """ Abstract method to get data for old seasons. """
        pass

    @abstractmethod
    def get_current_season_data(self):
        """ Abstract method to get data for the current season. """
        pass

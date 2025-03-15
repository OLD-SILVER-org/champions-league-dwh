import random
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logs.logger import ETLLogger

load_dotenv()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


class SeleniumScraper(ABC):
    """Selenium-based web scraper with configurable settings."""

    def __init__(self, headless=True, use_fake_agent=True):
        super().__init__()
        # Log
        self.logger = ETLLogger().get_logger()
        # Config
        self.config_option(headless, use_fake_agent)
        self.set_constants()

    def set_constants(self):
        print(f"START_SEASON: {os.getenv('START_SEASON')}")
        self.SAVE_PATH = os.getenv("SAVE_PATH")
        self.START_SEASON = int(os.getenv("START_SEASON"))
        self.current_season = self.get_current_season()

    def config_option(self, headless, use_fake_agent):
        """Configure options for the WebDriver."""
        self.options = Options()
        if headless:
            self.options.add_argument("--headless=new")
        # Random User-Agent
        if use_fake_agent:
            user_agent = random.choice(USER_AGENTS)
            self.options.add_argument(f"user-agent={user_agent}")
        # Anti-bot measures
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        # Ignore certificate SSL
        self.options.add_argument("--ignore-certificate-errors")

    def setup_driver(self):
        """Initialize WebDriver with options."""
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.options
        )

    def get_current_season(self):
        """Determine the current football season."""
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        return current_year - 1 if current_month <= 6 else current_year

    def get(self, url):
        """Open URL and wait."""
        self.setup_driver()
        self.driver.get(url)

    def find_element(self, by, value):
        """Find a single element."""
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        """Find multiple elements."""
        return self.driver.find_elements(by, value)

    def quit(self):
        """Close the WebDriver."""
        self.driver.quit()

    @abstractmethod
    def get_season_link(self, season):
        """Generate the FBref URL for a given season."""
        pass

    @abstractmethod
    def scrape_data(self, season):
        """Abstract method to scrape data for a given season."""
        pass

    @abstractmethod
    def save_data(self, dataframe, season):
        """Abstract method to save scraped data."""
        pass

    def scrape_data(self):
        return self.scrape_data(self.current_season)

    def get_current_season_data(self):
        """Scrape the current season's match data."""
        return self.scrape_data(self.current_season)

    def click_button(self, by, value):
        """Click button with minimal wait time."""
        try:
            button = self.driver.find_element(by, value)
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", button
            )  # Scroll nhanh
            button.click()
            self.logger.info("✅ Clicked button : %s", value)
        except Exception:
            self.logger.info(f"🔄 Normal click failed, trying JS click [{value}]")
            self.try_js_click(by, value)

    def try_js_click(self, by, value):
        """Try JavaScript click instantly if normal click fails."""
        try:
            button = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", button)
            self.logger.info("✅ JavaScript clicked button : %s", value)
        except Exception:
            self.logger.debug("❌ Completely failed to click button : %s", value)

    def close_cookie_banner(self):
        """Close the Osano cookie consent banner if it appears."""
        try:
            wait = WebDriverWait(self.driver, 1)
            accept_button = self.find_element(
                By.CLASS_NAME, "osano-cm-button--type_accept"
            )
            accept_button.click()
            self.logger.info("✅ Closed osano cookie consent popup")
        except Exception:
            self.logger.info("🔄 No cookie popup found, continuing...")

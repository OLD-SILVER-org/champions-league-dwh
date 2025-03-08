import re
from tasks.extract.web_scrapers.selenium_scraper import SeleniumScraper
import datetime
import pandas as pd
from selenium.webdriver.common.by import By
import sys
import os
from io import StringIO
import time


class PlayerScraper(SeleniumScraper):
    """Scraper for FBref football player data using Selenium."""

    def __init__(self):
        """Initialize SeleniumScraper and load environment variables."""
        super().__init__(headless=True, wait_time=1)
        self.PLAYERS_LOCATION = os.getenv("PLAYERS_LOCATION")

    pass

    def get_season_link(self, season):
        """Generate the FBref URL for a given season."""
        return f"https://fbref.com/en/comps/8/{season}-{season+1}/stats/{season}-{season+1}-Champions-League-Stats"

    def scrape_season_data(self):
        """Scrape player data for current season."""
        self.scrape_data(self.current_season)

    def scrape_data(self, season):
        """Abstract method to scrape data for a given season."""
        url = self.get_season_link(season)
        try:
            self.get(url)  # Open URL using SeleniumScraper
            self.close_cookie_banner()
            # Click the "Standard Stats" button
            self.click_button(By.ID, "stats_standard_control")
            # Find the player data table
            player_tbody = self.find_element(By.ID, "stats_standard").find_element(
                By.TAG_NAME, "tbody"
            )
            extracted_data = self.extract_player_data(player_tbody, season)
            self.save_data(extracted_data, season)
            return extracted_data
        except Exception as e:
            self.logger.error("❌ Scraping player failed for season %s : %s", season, e)
            return None
        finally:
            self.quit()

    def save_data(self, dataframe, season):
        """Abstract method to save scraped data."""
        now = datetime.datetime.now()
        folder_path = os.path.join(self.SAVE_PATH, self.PLAYERS_LOCATION, str(season))
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        )
        dataframe.to_csv(data_name, index=False)
        self.logger.info("✅ Data players saved: %s", data_name)
        pass

    def extract_player_data(self, player_tbody, season):
        """Extract player data from the table."""
        columns = [
            "Season",
            "Natural Key",
            "Name",
            "Nation",
            "Positions",
            "Squad_ID",
            "Squad",
            "Born",
        ]
        data = []  # Store extracted data as a list
        rows = player_tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            try:
                player_td = row.find_element(By.CSS_SELECTOR, 'td[data-stat="player"]')
                squad_td = row.find_element(By.CSS_SELECTOR, 'td[data-stat="team"]')

                # Extract data
                nk = player_td.get_attribute("data-append-csv") or ""
                name = player_td.get_attribute("textContent").strip()
                nation = (
                    row.find_element(By.CSS_SELECTOR, 'td[data-stat="nationality"]')
                    .get_attribute("textContent")
                    .strip()
                )
                positions = (
                    row.find_element(By.CSS_SELECTOR, 'td[data-stat="position"]')
                    .get_attribute("textContent")
                    .strip()
                )
                born = (
                    row.find_element(By.CSS_SELECTOR, 'td[data-stat="birth_year"]')
                    .get_attribute("textContent")
                    .strip()
                )

                # Extract Squad ID
                squad_href = (
                    squad_td.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if squad_td.find_elements(By.TAG_NAME, "a")
                    else ""
                )
                squad_id = re.search(r"/en/squads/([a-zA-Z0-9]+)/", squad_href)
                squad_id = squad_id.group(1) if squad_id else ""
                squad = squad_td.get_attribute("textContent").strip()

                # Append row data to list
                data.append(
                    [season, nk, name, nation, positions, squad_id, squad, born]
                )
            except Exception as e:
                self.logger.error("❌ Error processing row: %s", e)
        # Convert list to DataFrame once (better performance)
        df = pd.DataFrame(data, columns=columns)
        return df

from tasks.extract.web_scrapers.selenium_scraper import SeleniumScraper
import datetime
import pandas as pd
import random
import time

from selenium.webdriver.common.by import By
import sys
import os
from io import StringIO
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class MatchScraper(SeleniumScraper):
    """ Scraper for FBref football match data using Selenium. """

    def __init__(self):
        """ Initialize SeleniumScraper and load environment variables. """
        super().__init__(headless=True, wait_time=1)
        self.MATCHS_LOCATION = os.getenv("MATCHS_LOCATION")
        self.get_old_seasons_data()
    pass

    def get_season_link(self, season):
        """ Generate the FBref URL for a given season. """
        return f"https://fbref.com/en/comps/8/{season}-{season+1}/schedule/{season}-{season+1}-Champions-League-Stats-Scores-and-Fixtures"

    def save_data(self, dataframe, season):
        """ Save scraped data as a Parquet file. """
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.SAVE_PATH, self.MATCHS_LOCATION, str(season))
        print(f"📌 Folder path {folder_path}")
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        dataframe.to_csv(data_name, index=False)
        print(f"✅ Data saved: {data_name}")

    def scrape_data(self, season):
        """ Scrape match data for a given season using Selenium. """
        url = self.get_season_link(season)
        print(f"📌 Scraping season {season} link: {url}")

        try:
            self.get(url)  # Open URL using SeleniumScraper
            # Find the match data table
            table = self.find_element(
                By.CLASS_NAME, "stats_table").get_attribute("outerHTML")

            if not table:
                print(f"❌ No match data found for season {season}")
                return None

            print(f"✅ Successfully fetched page for season {season}")

            # Convert table to DataFrame
            # Pandas only return list of dataframes, [0] to get first
            dataframe = pd.read_html(StringIO(table))[0]

            # Save the DataFrame
            self.save_data(dataframe, season)
            # self.quit()  # Close Selenium WebDriver after scraping
            return dataframe

        except Exception as e:
            print(f"❌ Scraping failed for season {season}: {e}")
            return None

    def get_old_seasons_data(self):
        """ Scrape historical match data from past seasons. """
        list_old_seasons = list(
            range(self.START_SEASON, self.current_season))
        print(f"📌 List old seasons: {list_old_seasons}")
        # scrape data for each season
        for season in list_old_seasons:
            self.scrape_data(season)

    def get_current_season_data(self):
        """ Scrape the current season's match data. """
        return self.scrape_data(self.current_season)


# Test
if __name__ == "__main__":
    scraper = MatchScraper()
    scraper.get_current_season_data()
    scraper.quit()  # Close Selenium WebDriver after scraping
    # scraper.get_current_season_data()
    # scraper.quit()  # Close Selenium WebDriver after scraping

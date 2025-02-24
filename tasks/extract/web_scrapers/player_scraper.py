from selenium_scraper import SeleniumScraper
import datetime
import pandas as pd
from selenium.webdriver.common.by import By
import sys
import os
from io import StringIO
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class PlayerScraper(SeleniumScraper):
    """ Scraper for FBref football player data using Selenium. """

    def __init__(self):
        """ Initialize SeleniumScraper and load environment variables. """
        super().__init__(headless=True, wait_time=1)
        self.PLAYERS_LOCATION = os.getenv("PLAYERS_LOCATION")
        self.get_old_seasons_data()
    pass

    def get_season_link(self, season):
        """ Generate the FBref URL for a given season. """
        return f"https://fbref.com/en/comps/8/{season}-{season+1}/stats/{season}-{season+1}-Champions-League-Stats"

    def scrape_data(self, season):
        """ Abstract method to scrape data for a given season. """
        url = self.get_season_link(season)
        print(f"📌 Scraping season {season} link: {url}")

        try:
            self.get(url)  # Open URL using SeleniumScraper
            # Find the match data table
            playersTable = self.find_element(By.ID,
                                             "stats_standard").get_attribute("outerHTML")
            if not playersTable:
                print(f"❌ No player data found for season {season}")
                return None
            print(
                f"✅ Successfully fetched player for season {season}")

            # Convert table to DataFrame
            player_df = pd.read_html(StringIO(playersTable))[0]

            # Save the DataFrame
            self.save_data(player_df, season)
            # self.quit()  # Close Selenium WebDriver after scraping
            return player_df

        except Exception as e:
            print(f"❌ Scraping failed for season {season}: {e}")
            return None

    def save_data(self, dataframe, season):
        """ Abstract method to save scraped data. """
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.SAVE_PATH, self.PLAYERS_LOCATION, str(season))
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        dataframe.to_csv(data_name, index=False)
        print(f"✅ Data players saved: {data_name}")
        pass


if __name__ == "__main__":
    scraper = PlayerScraper()
    scraper.get_current_season_data()
    scraper.quit()
    pass

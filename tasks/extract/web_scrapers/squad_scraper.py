from selenium_scraper import SeleniumScraper
import datetime
import pandas as pd
from selenium.webdriver.common.by import By
import sys
import os
from io import StringIO
import re
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class SquadScraper(SeleniumScraper):
    """ Scraper for FBref football squad data using Selenium. """

    def __init__(self):
        """ Initialize SeleniumScraper and load environment variables. """
        super().__init__(headless=True, wait_time=1)
        self.SQUADS_LOCATION = os.getenv("SQUADS_LOCATION")
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
            self.get(url)
            # Find the match data table
            squad_tbody = self.find_element(
                By.ID, "stats_squads_standard_for").find_element(By.TAG_NAME, "tbody")
            if not squad_tbody:
                print(f"❌ No squad data found for season {season}")
                return None
            print(f"✅ Successfully fetched squad for season {season}")
            print(f"📌DEBUG 0")
            # Save the DataFrame
            extracted_data = self.extract_squad_data(squad_tbody)
            self.save_data(extracted_data, season)
            # Feature get more data in a row
            return extracted_data

        except Exception as e:
            print(f"❌ Scraping failed for season {season}: {e}")
            return None

    def save_data(self, dataframe, season):
        """ Abstract method to save scraped data. """
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.SAVE_PATH, self.SQUADS_LOCATION, str(season))
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        dataframe.to_csv(data_name, index=False)
        print(f"✅ Data squads saved: {data_name}")
        pass

    def extract_squad_data(self, squad_tbody):
        """ Extract squad data from the table. """
        # ✅ Define column names for the DataFrame
        columns = [
            "Natural Key",
            "Country",
            "Name",
            "Number Of Player",
            "Matches Played",
        ]
        df = pd.DataFrame(columns=columns)  # Initialize an empty DataFrame

        # ✅ Get all rows within the tbody element
        rows = squad_tbody.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            try:
                # ✅ Extract team name and country from the <th> tag
                th = row.find_element(By.TAG_NAME, "th")
                span = th.find_element(By.TAG_NAME, "span")
                a_tag = th.find_element(By.TAG_NAME, "a")

                # ✅ Get team name and country details
                href = a_tag.get_attribute("href")
                name = a_tag.text  # Get team name
                country = span.get_attribute("title")  # Get country name

                # ✅ Extract "Natural Key" from the href link
                match = re.search(r'/en/squads/([a-zA-Z0-9]+)/', href)
                nk = match.group(1) if match else ""

                # ✅ Extract the number of players used and matches played
                number_of_player = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="players_used"]').text
                matches_played = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="games"]').text

                # ✅ Append the extracted data into the DataFrame
                df = pd.concat([df, pd.DataFrame(
                    [[nk, country, name, number_of_player, matches_played]], columns=columns)], ignore_index=True)

                print(
                    f"📌 Data extracted: {nk, country, name, number_of_player, matches_played}")

            except Exception as e:
                # ✅ Log errors for debugging
                print(f"❌ Error processing row {row.text}: {e}")

        return df


if __name__ == "__main__":
    scraper = SquadScraper()
    scraper.get_current_season_data()
    scraper.quit()
    pass

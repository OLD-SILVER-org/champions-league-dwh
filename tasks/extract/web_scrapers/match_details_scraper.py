import re
from selenium_scraper import SeleniumScraper
import datetime
import pandas as pd
from selenium.webdriver.common.by import By
import sys
import os
from io import StringIO


class MatchDetailsScraper(SeleniumScraper):
    """ Scraper for FBref football squad details data using Selenium. """

    def __init__(self, match_id=0):
        """ Initialize SeleniumScraper and load environment variables. """
        super().__init__(headless=True, wait_time=1)
        self.MATCH_DETAILS_LOCATION = os.getenv("MATCH_DETAILS_LOCATION")
        self.match_id = match_id
    pass

    def get_season_link(self, season):
        return super().get_season_link(season)

    def get_match_link(self):
        """ Generate the FBref URL for match. """
        return f"https://fbref.com/en/matches/{self.match_id}"

    def scrape_data(self):
        """ Abstract method to scrape data for a given season. """
        url = self.get_match_link()
        print(f"📌 Scraping season {self.match_id} link: {url}")

        try:
            self.get(url)
            team_ids = self.get_team_ids()
            team_a_id, team_b_id = team_ids
            # Find the match data table
            match_tbody_a = self.find_element(
                By.ID, "a").find_element(By.TAG_NAME, "tbody")
            match_tbody_b = self.find_element(
                By.ID, "b").find_element(By.TAG_NAME, "tbody")
            if not match_tbody_a or not match_tbody_b:
                print(f"❌ No match data found for match  {self.match_id}")
                return None
            print(f"✅ Successfully fetched match  {self.match_id}")
            # Save the DataFrame
            extracted_data_a = self.extract_match_data(
                match_tbody_a, team_a_id)
            extracted_data_b = self.extract_match_data(
                match_tbody_b, team_b_id)
            extracted_data = pd.concat(
                [extracted_data_a, extracted_data_b], ignore_index=True)
            self.save_data(extracted_data)
            return extracted_data

        except Exception as e:
            print(f"❌ Scraping failed for match {self.match_id}: {e}")
            return None

    def get_team_ids(self):
        """ Get the teams id from the match. Call after Open the match page. """
        scorebox = self.find_element(By.CSS_SELECTOR, "div.scorebox")
        teams = scorebox.find_elements(By.CSS_SELECTOR, ".scorebox strong a")
        team_ids = [team.get_attribute("href").split("/")[-2]
                    for team in teams]
        team1_id, team2_id = team_ids
        return team_ids

    def save_data(self, dataframe):
        """ Abstract method to save scraped data. """
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.SAVE_PATH, self.MATCH_DETAILS_LOCATION)
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, str(self.match_id,) f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        dataframe.to_csv(data_name, index=False)
        print(f"✅ Data match saved: {data_name}")
        pass

    def extract_match_data(self, match_tbody, team_id):
        """ Extract match data from the table. """
        # ✅ Define column names for the DataFrame
        columns = ["match_id", "player_id", "shirt_number", "team_id",
                   "goals", "own_goals", "yellow_cards", "red_card", "bench"]

        df = pd.DataFrame(columns=columns)  # Initialize an empty DataFrame

        # ✅ Get all rows within the tbody element
        rows = match_tbody.find_elements(By.TAG_NAME, "tr")
        squad_team = []
        is_bench = False
        skip_first = True

        for row in rows:
            try:
                # Skip first line
                if skip_first:
                    skip_first = False
                    continue
                list_td = row.find_elements(By.TAG_NAME, "td")
                link = list_td[1].find_element(
                    By.TAG_NAME, "a").get_attribute("href")
                divs = list_td[1].find_elements(By.TAG_NAME, "div")

                # Extract player's information
                shirt_number = list_td[0].text
                player_id = link.split('/players/')[1].split('/')[0]
                goals = sum(
                    1 for div in divs if "goals" in div.get_attribute("class"))
                own_goals = sum(
                    1 for div in divs if "own_goals" in div.get_attribute("class"))
                yellow_cards = sum(
                    1 for div in divs if "yellow_card" in div.get_attribute("class"))
                red_card = sum(
                    1 for div in divs if "red_card" in div.get_attribute("class"))
                is_bench = bool(row.find("th"))

                # ✅ Add details into dict
                player_data = {
                    "match_id": self.match_id,  # You might need to pass match_id from somewhere
                    "player_id": player_id,
                    "shirt_number": shirt_number,  # Fixed missing comma in column definition
                    "team_id": team_id,
                    "goals": goals,
                    "own_goals": own_goals,
                    "yellow_cards": yellow_cards,
                    "red_card": red_card,
                    "bench": is_bench
                }
                # ✅ Append player data to DataFrame
                df = pd.concat(
                    [df, pd.DataFrame([player_data])], ignore_index=True)

            except Exception as e:
                # ✅ Log errors for debugging
                print(f"❌ Error extracting match data for team {team_id}: {e}")
                pass
        return df


# Test
if __name__ == "__main__":
    scraper = MatchDetailsScraper()
    scraper.match_id = "615d637e"
    scraper.scrape_data()
    scraper.quit()  # Close Selenium WebDriver after scraping

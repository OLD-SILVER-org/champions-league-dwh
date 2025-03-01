import re
import datetime
import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium_scraper import SeleniumScraper


class MatchDetailsScraper(SeleniumScraper):
    """ Scraper for FBref football match details using Selenium. """

    def __init__(self, match_id=0):
        """ Initialize SeleniumScraper and load environment variables. """
        super().__init__(headless=True, wait_time=1)
        self.MATCH_DETAILS_LOCATION = os.getenv("MATCH_DETAILS_LOCATION")
        self.MATCHS_LOCATION = os.getenv("MATCHS_LOCATION")
        self.match_id = match_id
        self.MATCH_ID_DETAILS_LOCATION = os.getenv("MATCH_ID_DETAILS_LOCATION")
        self.LV2_SAVE_PATH = os.getenv("LV2_SAVE_PATH")
        self.get_old_seasons_data()

    def get_match_link(self):
        """ Generate the FBref URL for the match. """
        return f"https://fbref.com/en/matches/{self.match_id}"

    def get_current_season_data(self):
        list_match_ids = self.get_list_match_by_season(self.get_current_season())
        for match_id in list_match_ids:
            self.match_id = match_id
            self.scrape_data()
        pass
        
    
    def scrape_data(self):
        """ Scrape match data and save to CSV. """
        url = self.get_match_link()
        print(f"📌 Scraping match {self.match_id} link: {url}")
        try:
            self.get(url)
            self.close_cookie_banner()
            team_ids = self.get_team_ids()
            team_a_id, team_b_id = team_ids
            print(f"{self.find_element(
                By.ID, "a").text}")
            # ✅ Find match data tables
            match_tbody_a = self.find_element(
                By.CSS_SELECTOR, "div.lineup#a").find_element(By.TAG_NAME, "tbody")
            print(f"📌 DEBUG :  {match_tbody_a.text}")
            match_tbody_b = self.find_element(
                By.CSS_SELECTOR, "div.lineup#b").find_element(By.TAG_NAME, "tbody")
            if not match_tbody_a or not match_tbody_b:
                print(f"❌ No match data found for match {self.match_id}")
                return None
            print(f"✅ Successfully fetched match {self.match_id}")
            # ✅ Extract and save data
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
        return

    def get_team_ids(self):
        """ Get the teams' IDs from the match page. """
        try:
            scorebox = self.find_element(By.CSS_SELECTOR, "div.scorebox")
            teams = scorebox.find_elements(
                By.CSS_SELECTOR, ".scorebox strong a")[:2]
            team_a = teams[0].get_attribute("href").split("/")[-2]
            team_b = teams[1].get_attribute("href").split("/")[-2]
            print(f"✅ Get two team id success!: {team_a}, {team_b}")
            return [team_a, team_b]
        except Exception as e:
            print(f"⚠️ Could not find two team IDs: {e}")
            return [None, None]

    def save_data(self, dataframe):
        """ Save scraped data to CSV. """
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.SAVE_PATH, self.MATCH_DETAILS_LOCATION, self.match_id)
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        dataframe.to_csv(data_name, index=False)
        print(f"✅ Data match saved: {data_name}")

    def extract_match_data(self, match_tbody, team_id):
        """ Extract match data from the table. """
        columns = ["match_id", "player_id", "shirt_number", "team_id",
                   "goals", "own_goals", "yellow_cards", "red_card", "bench"]

        player_list = []  # Store data before converting to DataFrame
        rows = match_tbody.find_elements(By.TAG_NAME, "tr")
        skip_first = True
        is_bench = False
        for row in rows:
            try:
                if skip_first:
                    skip_first = False
                    continue
                list_td = row.find_elements(By.TAG_NAME, "td")
                # Skip row not a player
                if len(list_td) < 2:
                    is_bench = True
                    print(
                        f"⚠️ Skipping row due to insufficient columns: {len(list_td)}")
                    continue
                link = list_td[1].find_element(
                    By.TAG_NAME, "a").get_attribute("href")
                divs = list_td[1].find_elements(By.TAG_NAME, "div")

                # ✅ Extract player details
                shirt_number = list_td[0].text
                player_id = link.split('/players/')[1].split('/')[0]
                goals = sum(
                    1 for div in divs if "goal" in div.get_attribute("class"))
                own_goals = sum(
                    1 for div in divs if "own_goal" in div.get_attribute("class"))
                yellow_cards = sum(
                    1 for div in divs if "yellow_card" in div.get_attribute("class"))
                red_card = sum(
                    1 for div in divs if "red_card" in div.get_attribute("class"))

                # ✅ Store data
                player_list.append({
                    "match_id": self.match_id,
                    "player_id": player_id,
                    "shirt_number": shirt_number,
                    "team_id": team_id,
                    "goals": goals,
                    "own_goals": own_goals,
                    "yellow_cards": yellow_cards,
                    "red_card": red_card,
                    "bench": is_bench
                })
            except Exception as e:
                print(f"❌ Error extracting match data for team {team_id}: {e}")

        # Convert list to DataFrame once
        return pd.DataFrame(player_list, columns=columns)
    
    def get_old_seasons_data(self):
        """Retrieve match IDs from past seasons and process them"""

        # Get the current season
        cur_season = self.get_current_season()

        # List all past seasons
        list_old_seasons = list(range(self.START_SEASON, cur_season))

        # Step 1: Collect all match IDs from past seasons
        all_match_ids = []
        for season in list_old_seasons:
            match_ids = self.get_list_match_by_season(season)
            if match_ids:
                all_match_ids.extend(match_ids)

        # Step 2: Process each match ID
        all_match_details = []
        for match_id in all_match_ids:
            self.match_id = match_id
            self.scrape_data()

        return all_match_details 

    def get_list_match_by_season(self, season):
        """Load transformed data from file"""
        path = os.path.join(
            self.LV2_SAVE_PATH, self.MATCHS_LOCATION, str(season), self.MATCH_ID_DETAILS_LOCATION)
        if not os.path.exists(path):
            print(f"⚠️ WARNING: Directory {path} does not exist!")
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        df = pd.read_csv(latest_file_path)
        match_ids = df["match_id"].tolist()
        return match_ids

    
    def get_season_link(self, season):
        return super().get_season_link(season)


# ✅ Test
if __name__ == "__main__":
    scraper = MatchDetailsScraper(match_id="19789895")
    scraper.get_current_season_data()
    # scraper.quit()  # Close Selenium WebDriver after scraping

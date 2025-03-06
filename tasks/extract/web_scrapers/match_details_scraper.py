import re
import datetime
import pandas as pd
import os
from selenium.webdriver.common.by import By
from tasks.extract.web_scrapers.selenium_scraper import SeleniumScraper


class MatchDetailsScraper(SeleniumScraper):
    """Scraper for FBref football match details using Selenium."""

    def __init__(self, match_id=0):
        """Initialize SeleniumScraper and load environment variables."""
        super().__init__(headless=True, wait_time=1)
        self.MATCH_DETAILS_LOCATION = os.getenv("MATCH_DETAILS_LOCATION")
        self.MATCHS_LOCATION = os.getenv("MATCHS_LOCATION")
        self.MATCH_ID_DETAILS_LOCATION = os.getenv("MATCH_ID_DETAILS_LOCATION")
        self.LV2_SAVE_PATH = os.getenv("LV2_SAVE_PATH")
        self.match_id = match_id
        # set default current season if not provided
        self.season = self.get_current_season()

    def get_match_link(self):
        """Generate the FBref URL for the match."""
        return f"https://fbref.com/en/matches/{self.match_id}"

    def scrape_season_data(self, season):
        list_match_ids = self.get_match_ids_transformed(season)
        for match_id in list_match_ids:
            # Set match_id, scrape data will use self attribute to run
            self.match_id = match_id
            self.scrape_data()
        pass

    def get_match_ids_transformed(self, season):
        """Load transformed match_ids data split to file after task matchTransforme run"""
        path = os.path.join(
            self.LV2_SAVE_PATH,
            self.MATCHS_LOCATION,
            str(season),
            self.MATCH_ID_DETAILS_LOCATION,
        )
        if not os.path.exists(path):
            self.logger.warning(f"⚠️ WARNING: Directory {path} does not exist!")
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        df = pd.read_csv(latest_file_path)
        match_ids = df["match_id"].tolist()
        return match_ids

    def scrape_data(self):
        """Scrape match data and save to CSV."""
        url = self.get_match_link()
        self.logger.info(f"📡 Scraping match {self.match_id} link: {url}")
        try:
            self.get(url)
            self.close_cookie_banner()
            team_ids = self.get_team_ids()
            team_a_id, team_b_id = team_ids
            # ✅ Find match data tables
            match_tbody_a = self.find_element(
                By.CSS_SELECTOR, "div.lineup#a"
            ).find_element(By.TAG_NAME, "tbody")
            match_tbody_b = self.find_element(
                By.CSS_SELECTOR, "div.lineup#b"
            ).find_element(By.TAG_NAME, "tbody")
            if not match_tbody_a or not match_tbody_b:
                self.logger.warning(f"⚠️ No match data found for match {self.match_id}")
                return None
            self.logger.info(f"✅ Successfully fetched match {self.match_id}")
            # ✅ Extract and save data
            extracted_data_a = self.extract_match_data(match_tbody_a, team_a_id)
            extracted_data_b = self.extract_match_data(match_tbody_b, team_b_id)
            extracted_data = pd.concat(
                [extracted_data_a, extracted_data_b], ignore_index=True
            )
            self.logger.info(f"✅ Data want to save for match {self.match_id}")
            self.save_data(extracted_data)
            return extracted_data
        except Exception as e:
            self.logger.error(f"❌ Scraping failed for match {self.match_id}: {e}")
            return None
        return

    def get_team_ids(self):
        """Get the teams' IDs from the match page."""
        try:
            scorebox = self.find_element(By.CSS_SELECTOR, "div.scorebox")
            teams = scorebox.find_elements(By.CSS_SELECTOR, ".scorebox strong a")[:2]

            def extract_team_id(team):
                """Extract team ID from squad URL using regex."""
                href = team.get_attribute("href")
                match = re.search(r"/squads/([^/]+)/", href)
                return match.group(1) if match else None

            team_ids = [extract_team_id(team) for team in teams]

            if all(team_ids):
                self.logger.info(
                    f"✅ Get two team IDs success!: {team_ids[0]}, {team_ids[1]}"
                )
            else:
                self.logger.warning("⚠️ One or both team IDs could not be extracted.")

            return team_ids

        except Exception as e:
            self.logger.error(f"❌ Could not find two team IDs: {e}")
            return [None, None]

    def save_data(self, dataframe):
        """Save scraped data to CSV."""
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.SAVE_PATH, self.MATCH_DETAILS_LOCATION, str(self.season), self.match_id
        )
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        )
        dataframe.to_csv(data_name, index=False)
        self.logger.info(f"✅ Data match saved: {data_name}")

    def extract_match_data(self, match_tbody, team_id):
        """Extract match data from the table."""
        columns = [
            "match_id",
            "player_id",
            "shirt_number",
            "team_id",
            "goals",
            "own_goals",
            "yellow_cards",
            "red_card",
            "bench",
        ]

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
                    self.logger.warning(
                        f"⚠️ Skipping row due to insufficient columns: {len(list_td)}"
                    )
                    continue
                link = list_td[1].find_element(By.TAG_NAME, "a").get_attribute("href")
                divs = list_td[1].find_elements(By.TAG_NAME, "div")

                # ✅ Extract player details
                shirt_number = list_td[0].text
                player_id = link.split("/players/")[1].split("/")[0]
                goals = sum(1 for div in divs if "goal" in div.get_attribute("class"))
                own_goals = sum(
                    1 for div in divs if "own_goal" in div.get_attribute("class")
                )
                yellow_cards = sum(
                    1 for div in divs if "yellow_card" in div.get_attribute("class")
                )
                red_card = sum(
                    1 for div in divs if "red_card" in div.get_attribute("class")
                )

                # ✅ Store data
                player_list.append(
                    {
                        "match_id": self.match_id,
                        "player_id": player_id,
                        "shirt_number": shirt_number,
                        "team_id": team_id,
                        "goals": goals,
                        "own_goals": own_goals,
                        "yellow_cards": yellow_cards,
                        "red_card": red_card,
                        "bench": is_bench,
                    }
                )
            except Exception as e:
                self.logger.error(
                    f"❌ Error extracting match data for team {team_id}: {e}"
                )

        # Convert list to DataFrame once
        return pd.DataFrame(player_list, columns=columns)

    def get_season_link(self, season):
        return super().get_season_link(season)


# ✅ Test
if __name__ == "__main__":
    scraper = MatchDetailsScraper(match_id="19789895")
    scraper.scrape_season_data("2024")
    # scraper.quit()  # Close Selenium WebDriver after scraping

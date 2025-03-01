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
            self.close_cookie_banner()
            # Find the match data table
            match_tbody = self.find_element(
                By.CLASS_NAME, "stats_table").find_element(By.TAG_NAME, "tbody")

            if not match_tbody:
                print(f"❌ No match data found for season {season}")
                return None

            print(f"✅ Successfully fetched page for season {season}")
            extracted_data = self.extract_match_data(match_tbody, season)
            self.save_data(extracted_data, season)
            return extracted_data

        except Exception as e:
            print(f"❌ Scraping failed for season {season}")
            return None

    def extract_match_data(self, match_tbody, season):
        """ Extract match data from the table. """
        columns = ["Season",
                   "Round", "Week", "Day", "Date", "Time",
                   "Home", "xG_Home", "Score", "xG_Away", "Away",
                   "Attendance", "Venue", "Referee", "Match Report"
                   ]
        df_list = []  # List to store extracted rows before converting to DataFrame
        rows = match_tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            try:
                # ✅ Extract match details
                round_text = row.find_element(By.TAG_NAME, "th").text
                week = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="gameweek"]').text
                day = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="dayofweek"]').text
                date = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="date"]').text
                time = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="start_time"]').text
                home = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="home_team"]').text
                score = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="score"]').text
                xG_Home_element = row.find_elements(By.CSS_SELECTOR, 'td[data-stat="home_xg"]')
                xG_Home = xG_Home_element[0].text if xG_Home_element else "" 

                xG_Away_element = row.find_elements(By.CSS_SELECTOR, 'td[data-stat="away_xg"]')
                xG_Away = xG_Away_element[0].text if xG_Away_element else ""
                away = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="away_team"]').text
                attendance = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="attendance"]').text
                venue = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="venue"]').text
                referee = row.find_element(
                    By.CSS_SELECTOR, 'td[data-stat="referee"]').text
                # ✅ Extract match report ID
                match_report = ""
                match_td = row.find_elements(
                    By.CSS_SELECTOR, 'td[data-stat="match_report"]')
                if match_td and match_td[0].find_elements(By.TAG_NAME, "a"):
                    match_href = match_td[0].find_element(
                        By.TAG_NAME, "a").get_attribute("href")
                    match_report = re.search(
                        r'/matches/([a-zA-Z0-9]+)/', match_href)
                    match_report = match_report.group(
                        1) if match_report else ""
                # ✅ Append to list
                df_list.append([season,
                                round_text, week, day, date, time, home, xG_Home, score,
                                xG_Away, away, attendance, venue, referee, match_report
                                ])
            except Exception as e:
                print(f"❌ Error processing row: {e}")
                continue
        # ✅ Convert list to DataFrame once
        return pd.DataFrame(df_list, columns=columns) if df_list else None


# Test
if __name__ == "__main__":
    scraper = MatchScraper()
    scraper.get_current_season_data()
    scraper.quit()  # Close Selenium WebDriver after scraping

import os
import sys
from abc import ABC, abstractmethod
import pandas as pd
from dotenv import load_dotenv
import datetime
from tasks.etl_old_data.base_old_etl import BaseOldETL

from tasks.extract.web_scrapers.match_details_scraper import MatchDetailsScraper

from tasks.transform.csv_transform.match_details_transformer import (
    MatchDetailsTransfomer,
)
from tasks.load.staging.match_details_loader import MatchDetailsLoader
from tasks.load.dwh.fact_match_loader import FactMatchLoader

load_dotenv()


class MatchOldETL(BaseOldETL):
    def __init__(self):
        super().__init__()
        # Attributes
        self.MATCH_DETAILS_LOCATION = os.getenv("MATCH_DETAILS_LOCATION")
        self.TABLE_MATCH_DETAILS = os.getenv("TABLE_MATCH_DETAILS")
        self.BIGQUERY_MATCH_DETAILS = os.getenv("BIGQUERY_MATCH_DETAILS")
        self.MATCHS_LOCATION = os.getenv("MATCHS_LOCATION")
        self.MATCH_ID_DETAILS_LOCATION = os.getenv("MATCH_ID_DETAILS_LOCATION")
        # Objects
        self.scraper = MatchDetailsScraper()
        self.transformer = MatchDetailsTransfomer()
        self.loader = MatchDetailsLoader()
        self.dwh_loader = FactMatchLoader()

    pass

    def extract(self):
        """Retrieve match IDs from past seasons and process them"""
        try:
            # Get the current season
            cur_season = self.get_current_season()
            # List all past seasons
            list_old_seasons = list(range(self.START_SEASON, cur_season + 1))
            # Step 1: Collect all match IDs from past seasons
            all_match_ids = []
            old_dict_match_ids = {}
            for season in list_old_seasons:
                self.logger.info(
                    f"📡  Start scraping match detail for season : {season}"
                )
                # Set season
                self.scraper.season = season
                self.scraper.scrape_season_data(season)
            self.logger.info("✅ Scraping match for old seasons completed.")
        except Exception as e:
            self.logger.error(f"❌ Scraping match for old seasons failed: {e}")

    def transform(self):
        list_old_seasons = list(range(self.START_SEASON, self.current_season + 1))
        for season in list_old_seasons:
            self.transformer.transform_data_by_season(str(season))
        pass

    def load(self):
        list_old_seasons = list(range(self.START_SEASON, self.current_season + 1))
        for season in list_old_seasons:
            self.loader.load_data_by_season(season)
        pass

    def load_to_dwh(self):
        self.dwh_loader.upload()

        pass


if __name__ == "__main__":
    pl = MatchOldETL()
    pl.extract()
    pl.transform()
    pl.load()
    # pl.load_to_dwh()

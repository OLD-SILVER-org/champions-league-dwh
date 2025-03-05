import os
import sys
from abc import ABC, abstractmethod
import pandas
from dotenv import load_dotenv
import datetime
from tasks.etl_old_data.base_old_etl import BaseOldETL

from tasks.extract.web_scrapers.match_scraper import MatchScraper

from tasks.transform.csv_transform.match_transformer import MatchTransformer
from tasks.load.staging.match_loader import MatchLoader
from tasks.load.dwh.fact_score_loader import FactScoreLoader

load_dotenv()


class ScoreOldETL(BaseOldETL):
    def __init__(self):
        super().__init__()
        # Attributes
        self.SCORES_LOCATION = os.getenv("SCORES_LOCATION")
        self.TABLE_SCORES = os.getenv("TABLE_SCORES")
        self.BIGQUERY_SCORES_FIXTURES = os.getenv("BIGQUERY_SCORES_FIXTURES")
        # Objects
        self.scraper = MatchScraper()
        self.transformer = MatchTransformer()
        self.loader = MatchLoader()
        self.dwh_loader = FactScoreLoader()

    pass

    def extract(self):
        list_old_seasons = list(range(self.START_SEASON, self.current_season))
        for season in list_old_seasons:
            self.scraper.scrape_data(season)
        pass

    def transform(self):
        list_old_seasons = list(range(self.START_SEASON, self.current_season))
        for season in list_old_seasons:
            self.transformer.transform_data(season)
        pass

    def load(self):
        list_old_seasons = list(range(self.START_SEASON, self.current_season))
        for season in list_old_seasons:
            self.loader.load_data(season)
        pass

    def load_to_dwh(self):
        self.dwh_loader.upload()

        pass


if __name__ == "__main__":
    pl = ScoreOldETL()
    # pl.extract()
    pl.transform()
    pl.load()
    pl.load_to_dwh()

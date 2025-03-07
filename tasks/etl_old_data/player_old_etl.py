import os
import sys
from abc import ABC, abstractmethod
import pandas
from dotenv import load_dotenv
import datetime
from tasks.etl_old_data.base_old_etl import BaseOldETL

from tasks.extract.web_scrapers.player_scraper import PlayerScraper

from tasks.transform.csv_transform.player_transformer import PlayerTransformer
from tasks.load.staging.player_loader import PlayerLoader
from tasks.load.dwh.dim_player_loader import DimPlayerLoader

load_dotenv()


class PlayerOldETL(BaseOldETL):
    def __init__(self):
        super().__init__()
        # Attributes
        self.PLAYERS_LOCATION = os.getenv("PLAYERS_LOCATION")
        self.TABLE_PLAYERS = os.getenv("TABLE_PLAYERS")
        self.BIGQUERY_PLAYERS = os.getenv("BIGQUERY_PLAYERS")
        # Objects
        self.scraper = PlayerScraper()
        self.transformer = PlayerTransformer()
        self.loader = PlayerLoader()
        self.dwh_loader = DimPlayerLoader()

    pass

    def extract(self):
        list_old_seasons = list(range(self.START_SEASON, self.current_season + 1))
        for season in list_old_seasons:
            self.scraper.scrape_data(season)
        pass

    def transform(self):
        list_old_seasons = list(range(self.START_SEASON, self.current_season + 1))
        for season in list_old_seasons:
            self.transformer.transform_data(season)
        pass

    def load(self):
        list_old_seasons = list(range(self.START_SEASON, self.current_season + 1))
        for season in list_old_seasons:
            self.loader.load_data(season)
        pass

    def load_to_dwh(self):
        self.dwh_loader.upload()

        pass


if __name__ == "__main__":
    pl = playerOldETL()
    pl.process()

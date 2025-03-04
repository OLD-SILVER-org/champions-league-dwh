import os
import sys
from abc import ABC, abstractmethod
import pandas
from dotenv import load_dotenv
import datetime
from tasks.etl_old_data.base_old_etl import BaseOldETL

from tasks.extract.web_scrapers.squad_scraper import SquadScraper

from tasks.transform.csv_transform.squad_transformer import SquadTransfomer
from tasks.load.staging.squad_loader import SquadLoader
from tasks.load.dwh.dim_squad_loader import DimSquadLoader

load_dotenv()


class SquadOldETL(BaseOldETL):
    def __init__(self):
        super().__init__()
        # Attributes
        self.SQUADS_LOCATION = os.getenv("SQUADS_LOCATION")
        self.TABLE_SQUADS = os.getenv("TABLE_SQUADS")
        self.BIGQUERY_SQUADS = os.getenv("BIGQUERY_SQUADS")
        # Objects
        self.scraper = SquadScraper()
        self.transformer = SquadTransfomer()
        self.loader = SquadLoader()
        self.dwh_loader = DimSquadLoader()

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
    pl = SquadOldETL()
    pl.extract()
    pl.transform()
    pl.load()
    pl.load_to_dwh()

from tasks.extract.web_scrapers.match_details_scraper import MatchDetailsScraper
from tasks.transform.csv_transform.match_details_transformer import (
    MatchDetailsTransfomer,
)
from tasks.load.staging.match_details_loader import MatchDetailsLoader
from tasks.load.dwh.fact_match_loader import FactMatchLoader


class ETL_match:
    def __init__(self):
        self.scraper = MatchDetailsScraper()
        self.transformer = MatchDetailsTransfomer()
        self.loader = MatchDetailsLoader()
        self.dim_loader = FactMatchLoader()

    def extract(self):
        self.scraper.scrape_season_data(self.scraper.season)

    def transform(self):
        self.transformer.transform_newest_data_by_season()

    def load(self):
        self.loader.load_newest_data_by_season()

    def load_to_dwh(self):
        self.dim_loader.upload()

    # Run
    def run(self):
        # self.extract()
        # self.transform()
        # self.load()
        self.load_to_dwh()


if __name__ == "__main__":
    etl = ETL_match()
    etl.run()

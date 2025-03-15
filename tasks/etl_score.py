from tasks.extract.web_scrapers.match_scraper import MatchScraper
from tasks.transform.csv_transform.match_transformer import MatchTransformer
from tasks.load.staging.match_loader import MatchLoader
from tasks.load.dwh.fact_score_loader import FactScoreLoader


class ETL_score:
    def __init__(self):
        self.scraper = MatchScraper()
        self.transformer = MatchTransformer()
        self.loader = MatchLoader()
        self.dim_loader = FactScoreLoader()

    def extract(self):
        self.scraper.scrape_season_data()

    def transform(self):
        self.transformer.transform_newest_data()

    def load(self):
        self.loader.load_newest_data()

    def load_to_dwh(self):
        self.dim_loader.upload()

    # Run
    def run(self):
        self.extract()
        self.transform()
        self.load()
        self.load_to_dwh()


if __name__ == "__main__":
    etl = ETL_score()
    etl.run()

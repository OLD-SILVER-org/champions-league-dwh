from tasks.extract.web_scrapers.player_scraper import PlayerScraper
from tasks.transform.csv_transform.player_transformer import PlayerTransformer
from tasks.load.staging.player_loader import PlayerLoader
from tasks.load.dwh.dim_player_loader import DimPlayerLoader


class ETL_player:
    def __init__(self):
        self.scraper = PlayerScraper()
        self.transformer = PlayerTransformer()
        self.loader = PlayerLoader()
        self.dim_loader = DimPlayerLoader()

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
    etl = ETL_player()
    etl.run()

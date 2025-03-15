from tasks.extract.web_scrapers.squad_scraper import SquadScraper
from tasks.transform.csv_transform.squad_transformer import SquadTransfomer
from tasks.load.staging.squad_loader import SquadLoader
from tasks.load.dwh.dim_squad_loader import DimSquadLoader


class ETL_squad:
    def __init__(self):
        self.scraper = SquadScraper()
        self.transformer = SquadTransfomer()
        self.loader = SquadLoader()
        self.dim_loader = DimSquadLoader()

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
    etl = ETL_squad()
    etl.run()

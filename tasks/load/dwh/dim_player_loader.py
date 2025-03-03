from bq_loader import BigQueryLoader
import os
from dotenv import load_dotenv

load_dotenv()


class DimPlayerLoader(BigQueryLoader):
    def __init__(self):
        super().__init__()
        self.BIGQUERY_PLAYERS = os.getenv("BIGQUERY_PLAYERS")

    def upload(self):
        self.upload_to_gbq(self.BIGQUERY_PLAYERS)
        return


if __name__ == "__main__":
    dsl = DimPlayerLoader()
    dsl.upload()

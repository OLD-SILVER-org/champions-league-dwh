from bq_loader import BigQueryLoader
import os
from dotenv import load_dotenv


class DimSquadLoader(BigQueryLoader):
    def __init__(self):
        super().__init__()
        self.BIGQUERY_SCORES_FIXTURES = os.getenv("BIGQUERY_SCORES_FIXTURES")

    def upload(self):
        self.upload_to_gbq(self.BIGQUERY_SCORES_FIXTURES)
        return


if __name__ == "__main__":
    dsl = DimSquadLoader()
    dsl.upload()

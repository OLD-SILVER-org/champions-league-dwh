from bq_loader import BigQueryLoader
import os
from dotenv import load_dotenv

load_dotenv()


class FactMatchLoader(BigQueryLoader):
    def __init__(self):
        super().__init__()
        self.BIGQUERY_MATCH_DETAILS = os.getenv("BIGQUERY_MATCH_DETAILS")

    def upload(self):
        self.upload_to_gbq(self.BIGQUERY_MATCH_DETAILS)
        return


if __name__ == "__main__":
    dsl = FactMatchLoader()
    dsl.upload()

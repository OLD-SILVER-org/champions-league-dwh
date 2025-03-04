import os
import sys
from abc import ABC, abstractmethod
import pandas
from dotenv import load_dotenv
import datetime
from logs.logger import ETLLogger

load_dotenv()


class BaseOldETL(ABC):
    def __init__(self):
        super().__init__()
        # Extract attributes
        self.SAVE_PATH = os.getenv("SAVE_PATH")
        self.START_SEASON = int(os.getenv("START_SEASON"))
        self.current_season = self.get_current_season()
        # Transform attributes
        self.LV2_SAVE_PATH = os.getenv("LV2_SAVE_PATH")
        # Load attributes
        self.TABLE_STATE = os.getenv("TABLE_STATE")
        self.BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")
        self.BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")
        # Log
        self.logger = ETLLogger().get_logger()
        pass

    def get_current_season(self):
        """Determine the current football season."""
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        return current_year - 1 if current_month <= 6 else current_year

    def extract(self):
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def process(self):
        self.extract()
        self.transform()
        self.load()
        pass

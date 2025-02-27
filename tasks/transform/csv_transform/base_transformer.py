import os
import pandas as pd
import time
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()


class BaseTransformer(ABC):
    def __init__(self):
        super().__init__()
        self.SAVE_PATH = os.getenv("SAVE_PATH")
        self.LV2_SAVE_PATH = os.getenv("LV2_SAVE_PATH")
        self.START_SEASON = os.getenv("START_SEASON")
        self.SQUADS_LOCATION = os.getenv("SQUADS_LOCATION")
        self.PLAYERS_LOCATION = os.getenv("PLAYERS_LOCATION")
        self.MATCH_DETAILS_LOCATION = os.getenv("MATCH_DETAILS_LOCATION")
        self.transform_old_data()

    def get_current_season(self):
        """ Determine the current football season. """
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        return current_year - 1 if current_month <= 6 else current_year

    def transform_newest_data(self):
        """Transform historical data from past seasons"""
        current_session = self.get_current_season()
        print(f"DEBUG CURENT SEASON {current_session}")
        return self.transform_data(current_session)

    def transform_old_data(self):
        """Transform historical data from past seasons"""
        list_old_seasons = list(
            range(int(self.START_SEASON), int(self.get_current_season())))
        for season in list_old_seasons:
            self.transform_data(season)
        pass

    @abstractmethod
    def transform_data(self, season):
        """Main transformation pipeline"""
        pass

    @abstractmethod
    def get_extracted_data(self):
        """Load extracted data from file"""
        pass

    @abstractmethod
    def standardize_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names & data types"""
        pass

    @abstractmethod
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean missing values, duplicates, and outliers"""
        pass

    @abstractmethod
    def add_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate primary and foreign keys"""
        pass

    @abstractmethod
    def create_relations(self):
        """Establish relationships between tables"""
        pass

    @abstractmethod
    def calculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute additional statistics or KPIs"""
        pass

    @abstractmethod
    def validate_data(self, df: pd.DataFrame) -> None:
        """Check data integrity and quality"""
        pass

    @abstractmethod
    def save_data(self, df: pd.DataFrame, path: str):
        """Save transformed data to a file"""
        pass

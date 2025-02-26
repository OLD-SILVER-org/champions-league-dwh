import os
import pandas as pd
import time
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseTransform(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def transform_data(self):
        """Main transformation pipeline"""
        pass

    @abstractmethod
    def get_extracted_data(self, path: str):
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

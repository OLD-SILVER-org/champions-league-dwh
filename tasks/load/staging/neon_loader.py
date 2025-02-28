from neon import NeonStagingDB as db
import sys
import os
from dotenv import load_dotenv
import datetime
import pandas as pd
from abc import ABC, abstractmethod

load_dotenv()


class NeonLoader(ABC):
    """Load transformed data into Neon PostgreSQL (Staging)"""

    def __init__(self):
        self.LV2_SAVE_PATH = os.getenv("LV2_SAVE_PATH")
        self.START_SEASON = os.getenv("START_SEASON")
        self.SQUADS_LOCATION = os.getenv("SQUADS_LOCATION")
        self.PLAYERS_LOCATION = os.getenv("PLAYERS_LOCATION")
        self.MATCH_DETAILS_LOCATION = os.getenv("MATCH_DETAILS_LOCATION")
        # self.SCORES_FIXTURES_LOCATION = os.getenv("MATCHS_LOCATION")
        # Neon Table names
        self.TABLE_PLAYERS = os.getenv("TABLE_PLAYERS")
        self.TABLE_SQUADS = os.getenv("TABLE_SQUADS")
        self.TABLE_MATCH_DETAILS = os.getenv("TABLE_MATCH_DETAILS")
        self.TABLE_SCORES_FIXTURES = os.getenv("TABLE_SCORES_FIXTURES")
        # connect to Neon
        self.db = db()
        self.db.connect()

    def get_current_season(self):
        """ Determine the current football season. """
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        return current_year - 1 if current_month <= 6 else current_year

    def load_newest_data(self):
        """load historical data from past seasons"""
        current_session = self.get_current_season()
        print(f"DEBUG CURENT SEASON {current_session}")
        return self.load_data(current_session)

    def load_old_data(self):
        """load historical data from past seasons"""
        list_old_seasons = list(
            range(int(self.START_SEASON), int(self.get_current_season())))
        for season in list_old_seasons:
            self.load_data(season)
        pass

    def load_csv(self, file_path, table_name, columns):
        """Upload CSV file to PostgreSQL using COPY FROM"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            with open(file_path, 'r', encoding='utf-8') as file:
                cursor.copy_expert(
                    f"COPY {table_name} ({', '.join(columns)}) FROM STDIN WITH CSV HEADER", file
                )

            conn.commit()
            cursor.close()
            conn.close()

            print(f"✅ Successfully loaded {file_path} into {table_name}")

        except Exception as e:
            print(f"❌ Failed to load {file_path} into {table_name}: {e}")

    @abstractmethod
    def load_data(self, season):
        """Main transform pipeline"""
        pass

    @abstractmethod
    def get_transformed_path(self):
        """Load transformed data from file"""
        pass

    def close(self):
        """Close DB connection"""
        self.db.close()

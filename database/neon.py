import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


class NeonStagingDB:
    """Manage connection to Neon PostgreSQL (Staging DB) using SQLAlchemy"""

    def __init__(self):
        self.db_url = os.getenv("NEON_URL")
        self.engine = None

    def connect(self):
        """Establish connection"""
        if self.engine is None:
            try:
                self.engine = create_engine(self.db_url)
                print("✅ Connected to Neon PostgreSQL")
            except Exception as e:
                print(f"❌ Connection failed: {e}")

    def load_data(self, df, table_name):
        """Load Pandas DataFrame into Neon PostgreSQL table using SQLAlchemy"""
        if self.engine is None:
            self.connect()
        try:
            df.to_sql(table_name, self.engine, if_exists="append", index=False)
            print(f"✅ Loaded {len(df)} records into {table_name}")
        except Exception as e:
            print(f"❌ Error loading data into {table_name}: {e}")

    def close(self):
        """Close database connection"""
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
            print("🔌 Connection closed.")


# Example usage
if __name__ == "__main__":
    staging = NeonStagingDB()
    staging.connect()

    # Load players.csv
    df_players = pd.read_csv("players.csv")
    staging.load_data(df_players, "players")

    # Load squads.csv
    df_squads = pd.read_csv("squads.csv")
    staging.load_data(df_squads, "squads")

    staging.close()

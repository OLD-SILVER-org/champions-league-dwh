import pandas as pd
from dotenv import load_dotenv
import datetime
import os
import sys
from pandas_gbq import to_gbq
from abc import ABC, abstractmethod

load_dotenv()
from database.neon import NeonStagingDB as neon
from database.google_big_query import GBQ as gbq
from logs.logger import ETLLogger


class BigQueryLoader(ABC):
    def __init__(self):
        self.gGBQ = gbq()
        self.source = neon()
        self.TABLE_STATE = os.getenv("TABLE_STATE")
        self.BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")
        self.BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")
        # log
        self.logger = ETLLogger().get_logger()

    def get_last_update(self, table_name):
        """Retrieve the last updated timestamp for a pipeline from state table."""
        query = "SELECT last_updated FROM {} WHERE pipeline_name = %s".format(
            self.TABLE_STATE
        )

        try:
            with self.source.get_connection().cursor() as cursor:
                cursor.execute(query, (table_name,))
                result = cursor.fetchone()
                if result:
                    self.logger.info("⏳ Last update for %s: %s", table_name, result[0])
                    return result[0]
                self.logger.warning("⏩ No last update found for %s", table_name)
                return None  # Handle case where no record is found

        except Exception as e:
            self.logger.error(
                "❌ Error fetching last update for %s: %s", table_name, e, exc_info=True
            )
            return None

    def get_newest_data(self, table_name):
        newest_TS = self.get_last_update(table_name)
        if newest_TS is None:
            return []  # Return empty list if no timestamp found
        result = self.get_neon_data(table_name, newest_TS)
        return result

    def get_neon_data(self, table_name, newest_TS):
        try:
            query = f"SELECT * FROM {table_name} WHERE updated_at >= %s"
            with self.source.get_connection().cursor() as cursor:
                cursor.execute(query, (newest_TS,))
                rows = cursor.fetchall()
                # Get columns from db
                columns = [desc[0] for desc in cursor.description]

                # Convert to DataFrame
                df = pd.DataFrame(rows, columns=columns)

                # Add updated_at
                df["updated_at"] = pd.to_datetime("now")

                cursor.close()
                return df

        except Exception as e:
            self.logger.error(f"❌ Error while fetching data from Neon: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    bql = BigQueryLoader()
    table_name = os.getenv("TABLE_SQUADS")
    print(f"Table name: {table_name}")

    bql.upload_to_gbq(table_name)

import pandas as pd
from dotenv import load_dotenv
import datetime
import os
import sys
from pandas_gbq import to_gbq

load_dotenv()

database_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "database")
)
sys.path.append(database_path)
from neon import NeonStagingDB as neon
from google_big_query import GBQ as gbq


class BigQueryLoader:
    def __init__(self):
        self.gGBQ = gbq()
        self.source = neon()
        self.TABLE_STATE = os.getenv("TABLE_STATE")
        self.BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")
        self.BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")

    def get_last_update(self, table_name):
        cursor = self.source.get_connection().cursor()
        try:
            cursor.execute(
                f"SELECT last_updated FROM {self.TABLE_STATE} WHERE pipeline_name = %s",
                (table_name,),  # Fix tuple issue
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            return None  # Handle case where no record is found
        finally:
            cursor.close()  # Ensure cursor is closed

    def get_newest_data(self, table_name):
        newest_TS = self.get_last_update(table_name)
        print(f" newest_TS :  {newest_TS}")
        if newest_TS is None:
            return []  # Return empty list if no timestamp found
        result = self.get_neon_data(table_name, newest_TS)
        return result

    def get_neon_data(self, table_name, newest_TS):
        try:
            query = f"SELECT * FROM {table_name} WHERE updated_at >= %s"

            with self.source.get_connection().cursor() as cursor:
                print(f"🔍 newest_TS value: {newest_TS} (type: {type(newest_TS)})")
                cursor.execute(query, (newest_TS,))

                rows = cursor.fetchall()
                # get collumn from neon
                columns = [desc[0] for desc in cursor.description]

            # Chuyển thành DataFrame
            df = pd.DataFrame(rows, columns=columns)
            df["updated_at"] = pd.to_datetime("now")
            return df

        except Exception as e:
            print(f"❌ Failed to get newest data from {table_name}: {e}")
            return None  # Ensure function returns something

    def upload_to_gbq(self, table_name):
        """Upload DataFrame to Google BigQuery."""
        table_id = f"{self.BIGQUERY_DATASET}.{table_name}"
        df = self.get_newest_data(table_name)
        try:
            to_gbq(
                df, table_id, project_id=self.BIGQUERY_PROJECT_ID, if_exists="append"
            )
            print(f"✅ Data uploaded to {table_id} successfully!")
        except Exception as e:
            print(f"❌ Error uploading data: {e}")


if __name__ == "__main__":
    bql = BigQueryLoader()
    table_name = os.getenv("TABLE_SQUADS")
    print(f"Table name: {table_name}")  # Debug xem table_name có đúng không

    last_update = bql.get_newest_data(table_name)
    print(last_update.head(10))
    bql.upload_to_gbq(table_name)

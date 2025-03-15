from tasks.load.dwh.bq_loader import BigQueryLoader
import os
from dotenv import load_dotenv
import uuid
from pandas_gbq import to_gbq

load_dotenv()


class FactMatchLoader(BigQueryLoader):
    def __init__(self):
        super().__init__()
        self.TABLE_MATCH_DETAILS = os.getenv("TABLE_MATCH_DETAILS")
        self.BIGQUERY_MATCH_DETAILS = os.getenv("BIGQUERY_MATCH_DETAILS")

    def upload(self):
        try:
            self.upload_to_gbq(self.BIGQUERY_MATCH_DETAILS, self.TABLE_MATCH_DETAILS)
            self.logger.info(
                f"🚀 Successfully uploaded data to {self.BIGQUERY_MATCH_DETAILS}"
            )
        except Exception as e:
            self.logger.error(
                "❌ Error uploading data to GBQ %s: %s",
                self.BIGQUERY_MATCH_DETAILS,
                e,
            )

        return

    def upload_to_gbq(self, table_name, pipeline_name):
        """Upload DataFrame to Google BigQuery."""
        table_id = f"{self.BIGQUERY_DATASET}.{table_name}"
        df = self.get_newest_data(pipeline_name)

        if df.empty:
            self.logger.warning("⚠️ No new data for %s. Skipping upload.", table_id)
            return

        self.logger.info(f"🔄 Uploading {len(df)} rows to {table_id}")

        # Rename columns
        column_mapping = {
            "match_id": "match_nk",
            "player_id": "player_nk",
            "team_id": "squad_nk",
        }

        df = df.rename(columns=column_mapping)
        # create unique id - String
        # df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]
        # Select required columns
        if "bench" in df.columns:
            df["bench"] = df["bench"].astype(int)

        df["match_nk"] = df["match_nk"].astype(str)
        df["player_nk"] = df["player_nk"].astype(str)
        df["squad_nk"] = df["squad_nk"].astype(str)

        # Upload to BigQuery
        try:
            to_gbq(
                df,
                table_id,
                project_id=self.BIGQUERY_PROJECT_ID,
                if_exists="append",
            )
            self.logger.info(f"✅ Successfully uploaded {len(df)} rows to {table_id}")
        except Exception as e:
            self.logger.error(f"❌ ERROR: Fail to update {table_id} \n: {e}")


if __name__ == "__main__":
    Dpl = FactScoreLoader()
    Dpl.upload()

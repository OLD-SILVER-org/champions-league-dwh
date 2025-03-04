from tasks.load.dwh.bq_loader import BigQueryLoader
import os
from dotenv import load_dotenv
from pandas_gbq import to_gbq

load_dotenv()


class DimSquadLoader(BigQueryLoader):
    def __init__(self):
        super().__init__()
        self.BIGQUERY_SQUADS = os.getenv("BIGQUERY_SQUADS")
        self.TABLE_SQUADS = os.getenv("TABLE_SQUADS")

    def upload(self):
        try:
            self.upload_to_gbq(self.BIGQUERY_SQUADS, self.TABLE_SQUADS)
            self.logger.info(f"🚀 Successfully uploaded data to {self.BIGQUERY_SQUADS}")
        except Exception as e:
            self.logger.error(
                "❌ Error uploading data to GBQ %s: %s", self.BIGQUERY_SQUADS, e
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
            "nk": "squad_nk",
            "name": "squad_name",
        }
        df = df.rename(columns=column_mapping)

        # Select required columns
        dim_squads_columns = [
            "id",
            "season",
            "squad_nk",
            "country",
            "squad_name",
            "number_of_player",
            "matches_played",
            "updated_at",
        ]
        df = df[dim_squads_columns]

        # Upload to BigQuery
        to_gbq(
            df,
            table_id,
            project_id=self.BIGQUERY_PROJECT_ID,
            if_exists="append",
        )

        self.logger.info(f"✅ Successfully uploaded {len(df)} rows to {table_id}")


if __name__ == "__main__":
    Dpl = DimPlayerLoader()
    Dpl.upload()

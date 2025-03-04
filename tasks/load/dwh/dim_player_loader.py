from tasks.load.dwh.bq_loader import BigQueryLoader
import os
from dotenv import load_dotenv
from pandas_gbq import to_gbq

load_dotenv()


class DimPlayerLoader(BigQueryLoader):
    def __init__(self):
        super().__init__()
        self.BIGQUERY_PLAYERS = os.getenv("BIGQUERY_PLAYERS")
        self.TABLE_PLAYERS = os.getenv("TABLE_PLAYERS")

    def upload(self):
        try:
            self.upload_to_gbq(self.BIGQUERY_PLAYERS, self.TABLE_PLAYERS)
            self.logger.info(
                f"🚀 Successfully uploaded data to {self.BIGQUERY_PLAYERS}"
            )
        except Exception as e:
            self.logger.error(
                "❌ Error uploading data to GBQ %s: %s", self.BIGQUERY_PLAYERS, e
            )

        return

    def upload_to_gbq(self, table_name, pipeline_name):
        """Upload DataFrame to Google BigQuery."""
        table_id = f"{self.BIGQUERY_DATASET}.{table_name}"
        df = self.get_newest_data(pipeline_name)
        if df.empty:
            self.logger.warning("No new data for %s. Skipping upload.", table_id)
            return
            self.logger.info(f"Uploading {len(df)} rows to {table_id}")
            # Rename columns
            column_mapping = {
                "nk": "player_nk",
                "squad_id": "squad_nk",
                "squad": "squad_name",
            }
            df = df.rename(columns=column_mapping)
            # Mapping columns
            dim_players_columns = [
                "id",
                "season",
                "player_nk",
                "name",
                "nation",
                "positions",
                "squad_nk",
                "squad_name",
                "born",
            ]
            # Mappig tables
            df = df[dim_players_columns]
            # Upload to BigQuery
            to_gbq(
                df,
                table_id,
                project_id=self.BIGQUERY_PROJECT_ID,
                if_exists="append",
                table_schema=[{"name": "squad_id", "type": "STRING"}],
            )


if __name__ == "__main__":
    Dpl = DimPlayerLoader()
    Dpl.upload()

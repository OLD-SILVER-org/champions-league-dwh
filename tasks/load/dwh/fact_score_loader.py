from tasks.load.dwh.bq_loader import BigQueryLoader
import os
from dotenv import load_dotenv
from pandas_gbq import to_gbq
import uuid

load_dotenv()


class FactScoreLoader(BigQueryLoader):
    def __init__(self):
        super().__init__()
        self.BIGQUERY_SCORES_FIXTURES = os.getenv("BIGQUERY_SCORES_FIXTURES")
        self.TABLE_SCORES_FIXTURES = os.getenv("TABLE_SCORES_FIXTURES")

    def upload(self):
        try:
            self.upload_to_gbq(
                self.BIGQUERY_SCORES_FIXTURES, self.TABLE_SCORES_FIXTURES
            )
            self.logger.info(
                f"🚀 Successfully uploaded data to {self.BIGQUERY_SCORES_FIXTURES}"
            )
        except Exception as e:
            self.logger.error(
                "❌ Error uploading data to GBQ %s: %s",
                self.BIGQUERY_SCORES_FIXTURES,
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
            "home": "home_squad",
            "away": "away_squad",
            "xg_home": "xg_home_squad",
            "xg_away": "xg_away_squad",
            "match_report": "match_nk",
        }
        df = df.rename(columns=column_mapping)
        # create unique id - String
        df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]
        # Select required columns
        fact_scores_columns = [
            "id",
            "season",
            "round",
            "week",
            "day",
            "home_squad",
            "xg_home_squad",
            "xg_away_squad",
            "away_squad",
            "attendance",
            "venue",
            "referee",
            "match_nk",
            "match_datetime",
            "home_score",
            "away_score",
            "updated_at",
        ]
        df = df[fact_scores_columns]
        # Upload to BigQuery
        try:
            to_gbq(
                df,
                table_id,
                project_id=self.BIGQUERY_PROJECT_ID,
                if_exists="append",
            )
        except Exception as e:
            print(f"ERROT: {e}")
        self.logger.info(f"✅ Successfully uploaded {len(df)} rows to {table_id}")


if __name__ == "__main__":
    Dpl = FactScoreLoader()
    Dpl.upload()

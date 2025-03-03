from dotenv import load_dotenv
import os
from google.cloud import bigquery

load_dotenv()


class GBQ:
    def __init__(self):
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.project_id = os.getenv("BIGQUERY_PROJECT_ID")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        self.client = bigquery.Client()
        self.BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")
        pass

    def try_get_dataset(self):
        try:
            datasets = list(self.client.list_datasets(project=self.project_id))
            if datasets:
                print("✅ Connect Success, list dataset:")
                for dataset in datasets:
                    print(f"- {dataset.dataset_id}")
            else:
                print("✅Connect Success, but dont have any dataset in project.")
        except Exception as e:
            print("❌ Connect Fail to BigQuery:", e)


if __name__ == "__main__":
    gbq = GBQ()
    gbq.try_get_dataset()

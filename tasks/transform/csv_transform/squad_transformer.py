import os
import pandas as pd
from base_transformer import BaseTransformer
import datetime


class SquadTransfomer(BaseTransformer):
    def __init__(self):
        """Initialize SquadTransfomer."""
        super().__init__()
        self.SQUADS_LOCATION = os.getenv("SQUADS_LOCATION")
        self.transform_old_data()

    def transform_data(self, season: str):
        """Run the entire transformation pipeline from extraction to storage."""
        print("🔄 Starting data transformation pipeline...")

        # 1. Load raw data
        df = self.get_extracted_data(season)
        print("✅ Data loaded successfully!")

        # 2. Standardize schema (rename columns, fix data types, etc.)
        df = self.standardize_schema(df)
        print("✅ Schema standardized!")

        # 3. Clean data (remove nulls, duplicates, handle outliers)
        df = self.clean_data(df)
        print("✅ Data cleaned!")

        # 4. Add primary and foreign keys
        df = self.add_keys(df)
        print("✅ Keys added!")

        # 5. Create relationships between tables
        self.create_relations(df)
        print("✅ Relationships created!")

        # 6. Compute additional statistics (KPIs, derived metrics, etc.)
        df = self.calculate_metrics(df)
        print("✅ Metrics calculated!")

        # 7. Validate data integrity (check for missing or incorrect values)
        df = self.validate_data(df)
        print("✅ Data validated!")
        print(f"{df.head()}")

        # 8. Save transformed data to file
        df = self.save_data(df, season)
        print("🚀 Data transformation pipeline completed!")
        return df

    def get_extracted_data(self, season) -> pd.DataFrame:
        """Load extracted data from CSV file."""
        path = os.path.join(
            self.SAVE_PATH, self.SQUADS_LOCATION, str(season))
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        return pd.read_csv(latest_file_path)

    def standardize_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize schema for squad data."""
        # Convert column names to lowercase
        df.columns = df.columns.str.lower()
        # Rename 'Natural Key' column to 'nk'
        df = df.rename(columns={"natural key": "nk"})
        # Standardize country names (capitalize first letter, strip spaces)
        if 'country' in df.columns:
            df['country'] = df['country'].str.strip().str.title()

        # Standardize team name (strip spaces, check encoding if needed)
        if 'name' in df.columns:
            df['name'] = df['name'].str.strip()

        # Convert number_of_player and matches_played to integer
        for col in ['number of player', 'matches played']:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col], errors='coerce').astype('Int64')

        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove missing values, duplicates, and handle inconsistencies in squad data."""
        initial_rows = len(df)

        # 1. Remove rows with missing values in important columns
        print(f"{df.head()}")
        important_cols = ['nk', 'name', 'country', 'season']
        df = df.dropna(subset=important_cols)

        # 2. Remove duplicate rows based on important columns
        df = df.drop_duplicates(subset=important_cols, keep='first')

        # 3. Ensure season is valid (non-negative integer)
        if 'season' in df.columns:
            df = df[df['season'].astype('Int64') >= 0]

        # Log total rows removed
        final_rows = len(df)
        removed_rows = initial_rows - final_rows
        print(f"✅ DEBUG: Squad Data Cleaning Done!")
        print(f"✅ Total rows removed: {removed_rows} / {initial_rows}")
        return df

    def add_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate primary and foreign keys for relational integrity."""
        """Squad (SQUADS) is a dim data, have nk at Extract process -> dont need more"""
        return df

    def create_relations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Define relationships between different tables."""

        # TODO : Create relations with dim tables - Not yet!
        return df

    def calculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute additional statistics or KPIs for analysis."""
        # TODO : Create additional statistics for analysis - Not yet!
        return df

    def validate_data(self, df: pd.DataFrame) -> None:
        """Perform data integrity and quality checks."""
        """Ensure NK column has valid data, remove rows if NK is missing."""
        initial_rows = len(df)
        # Remove rows where NK is missing or null
        df = df.dropna(subset=['nk'])

        final_rows = len(df)
        removed_rows = initial_rows - final_rows
        print(f"✅ DEBUG: Squad Data Validation Done!")
        print(
            f"✅ Total rows removed due to missing NK: {removed_rows} / {initial_rows}")

        return df

    def save_data(self, df: pd.DataFrame, season):
        """Save transformed data to a CSV file."""
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.LV2_SAVE_PATH, self.SQUADS_LOCATION, str(season))
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        df.to_csv(data_name, index=False)
        return df


if __name__ == "__main__":
    transfomer = SquadTransfomer()
    df = transfomer.transform_newest_data()
    print(f"{df.head}")

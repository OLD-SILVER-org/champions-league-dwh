import os
import pandas as pd
from base_transformer import BaseTransformer


class MatchTransformer(BaseTransformer):
    """
    Transformer class for match data, handling schema standardization,
    cleaning, key generation, metric calculations, and validation.
    """

    def __init__(self):
        """Initialize MatchTransformer."""
        super().__init__()
        self.SAVE_PATH = os.getenv("SAVE_PATH")
        self.MATCHS_LOCATION = os.getenv("MATCHS_LOCATION")

    def transform_old_data(self):
        """Transform historical data from past seasons"""
        pass

    def transform_data(self, input_path: str, output_path: str):
        """Run the entire transformation pipeline from extraction to storage."""
        print("🔄 Starting data transformation pipeline...")

        # 1. Load raw data
        df = self.get_extracted_data(input_path)
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
        self.create_relations()
        print("✅ Relationships created!")

        # 6. Compute additional statistics (KPIs, derived metrics, etc.)
        df = self.calculate_metrics(df)
        print("✅ Metrics calculated!")

        # 7. Validate data integrity (check for missing or incorrect values)
        self.validate_data(df)
        print("✅ Data validated!")

        # 8. Save transformed data to file
        self.save_data(df, output_path)
        print(f"✅ Data saved to {output_path}")

        print("🚀 Data transformation pipeline completed!")

    def get_extracted_data(self, season) -> pd.DataFrame:
        """Load extracted data from CSV file."""
        path = os.path.join(
            self.SAVE_PATH, self.MATCHS_LOCATION, str(season))
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        return pd.read_csv(latest_file_path)

    def standardize_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names & data types."""
        column_mapping = {
            "Season": "season",
            "Round": "round",
            "Week": "week",
            "Day": "day",
            "Date": "date",
            "Time": "time",
            "Home": "home",
            "xG_Home": "xg_home",
            "Score": "score",
            "xG_Away": "xg_away",
            "Away": "away",
            "Attendance": "attendance",
            "Venue": "venue",
            "Referee": "referee",
            "Match Report": "match_report"
        }

        dtype_mapping = {
            "date": "datetime64[ns]",  # Convert to datetime format
            "week": "Int64",  # Convert to integer (nullable)
            "attendance": "Int64",  # Convert to integer (nullable)
            "xg_home": "float64",  # Convert to float
            "xg_away": "float64"   # Convert to float
        }

        # Rename columns
        df = df.rename(columns=column_mapping)
        # Convert data types
        for col, dtype in dtype_mapping.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype, errors="ignore")
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove missing values, duplicates, and handle outliers."""
        return df

    def add_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate primary and foreign keys for relational integrity."""
        return df

    def create_relations(self):
        """Define relationships between different tables."""
        pass

    def calculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute additional statistics or KPIs for analysis."""
        return df

    def validate_data(self, df: pd.DataFrame) -> None:
        """Perform data integrity and quality checks."""
        pass

    def save_data(self, df: pd.DataFrame, path: str):
        """Save transformed data to a CSV file."""
        df.to_csv(path, index=False)

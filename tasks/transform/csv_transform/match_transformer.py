import os
import pandas as pd
from base_transformer import BaseTransformer
import datetime


class MatchTransformer(BaseTransformer):
    """
    Transformer class for match data, handling schema standardization,
    cleaning, key generation, metric calculations, and validation.
    """

    def __init__(self):
        """Initialize MatchTransformer."""
        super().__init__()
        self.MATCHS_LOCATION = os.getenv("MATCHS_LOCATION")
        self.MATCH_ID_DETAILS_LOCATION =  str(os.getenv("MATCH_ID_DETAILS_LOCATION"))
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
            self.SAVE_PATH, self.MATCHS_LOCATION, str(season))
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        print(f"✅ DEBUG : path {latest_file_path}")
        return pd.read_csv(latest_file_path)

    def standardize_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize schema and split score column into home_score and away_score."""
        # Convert column names to lowercase
        df.columns = df.columns.str.lower()
        print(f"{df.columns}")
        print(f"{df['date'].head(10)}")

        # Convert column week to int
        df['week'] = df['week'].astype('Int64')
        # Normalize datetime
        if 'date' in df.columns and 'time' in df.columns:
            df['time'] = df['time'].str.extract(r'\((\d{2}:\d{2})\)')
            df['time'] = df['time'].fillna('00:00')
            df['match_datetime'] = pd.to_datetime(
                df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M', errors='coerce')
            df.drop(columns=['date', 'time'], inplace=True, errors='ignore')
        # Normalize "home" and "away" columns (remove country prefix)
        # Example: "eng Aston Villa" → "Aston Villa"
        df["home"] = df["home"].str.replace(r"\s[a-z]{2,3}$", "", regex=True)
        df["away"] = df["away"].str.replace(r"^[a-z]{2,3}\s", "", regex=True)

        # Standardize score column by splitting into home_score and away_score
        df[['home_score', 'away_score']] = df['score'].str.split(
            '–', expand=True).astype('Int64')
        df.drop(columns=['score'], inplace=True)
        # Convert attendance to string and remove non-numeric characters (e.g., ',', 'k', etc.)
        df['attendance'] = (df['attendance']
                            .astype(str)
                            # Keep only digits
                            .str.replace(r'[^\d]', '', regex=True)
                            # Replace empty strings with NaN
                            .replace('', pd.NA)
                            .astype('Int64'))
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize dataset before loading into DB."""
        initial_rows = len(df)

        # 1. Rename columns to match database schema
        column_mapping = {
            "match report": "match_report"
        }
        df.rename(columns=column_mapping, inplace=True)

        # 2. Drop rows with missing values in important columns
        important_cols = ["season", "home", "home_score",
                          "away", "away_score", "match_report"]
        df = df.dropna(subset=important_cols)

        # 3. Convert data types
        df["season"] = pd.to_numeric(
            df["season"], errors="coerce").astype("Int64")
        df["week"] = pd.to_numeric(
            df["week"], errors="coerce").astype("Float64")

        # 4. Remove duplicate rows (keeping the first occurrence)
        df = df.drop_duplicates(subset=important_cols, keep="first")

        # 5. Ensure numeric values are valid
        df = df[(df["xg_home"] >= 0) & (df["xg_away"] >= 0)]

        # Log total rows removed
        final_rows = len(df)
        removed_rows = initial_rows - final_rows
        print(f"✅ DEBUG: Clean Done!")
        print(f"✅ Total rows removed: {removed_rows} / {initial_rows}")

        return df

    def add_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate primary and foreign keys for relational integrity."""
        """Match (SQUAD AND FIXTURES) is a Fact data - > dont need add key, this will auto add when load to db Staging"""
        return df

    def create_relations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Define relationships between different tables."""

        # TODO : Create relations with dim tables - Not yet!
        return df

    def calculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute additional statistics or KPIs for analysis."""
        # TODO : Create additional statistics for analysis - Not yet!
        return df

    def validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform data integrity and quality checks."""
        # TODO  validate data but clean do most -> not yet
        return df

    def save_data(self, df: pd.DataFrame, season):
        """Save transformed data to a CSV file."""
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.LV2_SAVE_PATH, self.MATCHS_LOCATION, str(season))
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        df.to_csv(data_name, index=False)
        self.split_match_id(df,season)
        return df
    
    
    def split_match_id(self,df,season):
        """Split match id to a csv file"""
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.LV2_SAVE_PATH, self.MATCHS_LOCATION, str(season), self.MATCH_ID_DETAILS_LOCATION)
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv")
        df[["match_report"]].rename(columns={"match_report": "match_id"}).to_csv(data_name, index=False)
        return df

if __name__ == "__main__":
    transfomer = MatchTransformer()
    transfomer.transform_newest_data()

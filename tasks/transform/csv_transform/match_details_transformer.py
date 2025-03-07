import os
import pandas as pd
from tasks.transform.csv_transform.base_transformer import BaseTransformer
import datetime


class MatchDetailsTransfomer(BaseTransformer):
    def __init__(self, match_id=0, season="2017"):
        """Initialize MatchDetailsTransfomer."""
        super().__init__()
        self.MATCH_DETAILS_LOCATION = os.getenv("MATCH_DETAILS_LOCATION")
        self.match_id = match_id
        self.season = self.get_current_season()

    def transform_newest_data_by_season(self):
        self.transform_data_by_season(str(self.season))

    def transform_data_by_season(self, season):
        """Transform data for all matches in a season."""
        match_data = self.get_extracted_data_by_season(season)  # {match_id: DataFrame}

        if not match_data:
            self.logger.warning(f"No data found for season {season}")
            return {}

        transformed_data = {}
        for match_id in match_data:
            df = self.transform_data(match_id, season)
            if df is not None:
                transformed_data[match_id] = df

        return transformed_data

    def transform_newest_data(self, match_id):
        self.transform_data(match_id, self.get_current_season())

        pass

    def transform_data(self, match_id: str, season):
        self.match_id = match_id
        """Run the entire transformation pipeline from extraction to storage."""
        self.logger.info("🔄 Starting data transformation pipeline...")

        # 1. Load raw data
        df = self.get_extracted_data(self.match_id, season)
        self.logger.info("✅ Data loaded successfully!")

        # 2. Standardize schema (rename columns, fix data types, etc.)
        df = self.standardize_schema(df)
        self.logger.info("✅ Schema standardized!")

        # 3. Clean data (remove nulls, duplicates, handle outliers)
        df = self.clean_data(df)
        self.logger.info("✅ Data cleaned!")

        # 4. Add primary and foreign keys
        df = self.add_keys(df)
        self.logger.info("✅ Keys added!")

        # 5. Create relationships between tables
        self.create_relations(df)
        self.logger.info("✅ Relationships created!")

        # 6. Compute additional statistics (KPIs, derived metrics, etc.)
        df = self.calculate_metrics(df)
        self.logger.info("✅ Metrics calculated!")

        # 7. Validate data integrity (check for missing or incorrect values)
        df = self.validate_data(df)
        self.logger.info("✅ Data validated!")

        # 8. Save transformed data to file
        df = self.save_data(df, self.match_id, season)
        self.logger.info("🚀 Data transformation pipeline completed!")
        return df

    def get_extracted_data_by_season(self, season) -> dict:
        """Load extracted data for all matches in a season, return as a dict {match_id: DataFrame}."""
        season_path = os.path.join(self.SAVE_PATH, self.MATCH_DETAILS_LOCATION, season)

        if not os.path.exists(season_path):
            self.logger.warning(f"Season path does not exist: {season_path}")
            return {}

        match_ids = [
            d
            for d in os.listdir(season_path)
            # Skip if the item is not a directory
            if os.path.isdir(os.path.join(season_path, d))
        ]
        if not match_ids:
            logging.warning(f"No match data found for season {season}")
            return {}
        # Load data for each match
        match_data_dict = {}
        for match_id in match_ids:
            df = self.get_extracted_data(match_id, season)
            if df is not None:
                match_data_dict[match_id] = df
            else:
                logging.warning(
                    f"Failed to load data for match {match_id} in season {season}"
                )

        return match_data_dict

    def get_extracted_data(self, match_id, season) -> pd.DataFrame:
        """Load extracted data from CSV file."""
        path = os.path.join(
            self.SAVE_PATH, self.MATCH_DETAILS_LOCATION, season, str(match_id)
        )
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        return pd.read_csv(latest_file_path)

    def standardize_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize schema for match details data."""
        # Convert column names to lowercase
        df.columns = df.columns.str.lower()

        # Standardize team and referee names (capitalize first letter of each word)
        for col in ["team", "referee"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.title()

        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove missing values, duplicates, and handle inconsistencies in match details data."""
        initial_rows = len(df)
        # 1. Remove rows with missing values in all columns
        important_cols = df.columns.tolist()
        df = df.dropna(subset=important_cols)
        # 2. Remove duplicate rows based on all columns
        df = df.drop_duplicates(keep="first")
        # 3. Ensure all numerical values are non-negative
        for col in df.select_dtypes(include=["number"]).columns:
            df = df[df[col] >= 0]
        # Log total rows removed
        final_rows = len(df)
        removed_rows = initial_rows - final_rows
        self.logger.info(f"✅Match Details Cleaning Done!")
        self.logger.info(f"✅ Total rows removed: {removed_rows} / {initial_rows}")

        return df

    def add_keys(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate primary and foreign keys for relational integrity."""
        """Player (SQUADS) is a dim data, have nk at Extract process -> dont need more"""
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
        """Clean method do the most -> do nothing"""
        return df

    def save_data(self, df: pd.DataFrame, match_id, season):
        """Save transformed data to a CSV file."""
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.LV2_SAVE_PATH, self.MATCH_DETAILS_LOCATION, season, str(match_id)
        )
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        )
        df.to_csv(data_name, index=False)
        return df


if __name__ == "__main__":
    transfomer = MatchDetailsTransfomer("0c2a0842")
    # df = transfomer.transform_data("19789895")
    # print(f"{df.head}")
    # df = transfomer.get_extracted_data("0c2a0842", "2024")
    # print(f"DEBUG {df.head(10)}")
    df = transfomer.transform_data_by_season("2024")

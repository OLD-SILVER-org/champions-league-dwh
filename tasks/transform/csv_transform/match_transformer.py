import os
import pandas as pd
from tasks.transform.csv_transform.base_transformer import BaseTransformer
import datetime
import re


class MatchTransformer(BaseTransformer):
    """
    Transformer class for match data, handling schema standardization,
    cleaning, key generation, metric calculations, and validation.
    """

    def __init__(self):
        """Initialize MatchTransformer."""
        super().__init__()
        self.MATCHS_LOCATION = os.getenv("MATCHS_LOCATION")
        self.MATCH_ID_DETAILS_LOCATION = str(os.getenv("MATCH_ID_DETAILS_LOCATION"))

    def transform_data(self, season: str):
        """Run the entire transformation pipeline from extraction to storage."""
        self.logger.info("🔄 Starting data transformation pipeline...")

        # 1. Load raw data
        df = self.get_extracted_data(season)
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
        df = self.save_data(df, season)
        self.logger.info("🚀 Data transformation pipeline completed!")
        return df

    def get_extracted_data(self, season) -> pd.DataFrame:
        """Load extracted data from CSV file."""
        path = os.path.join(self.SAVE_PATH, self.MATCHS_LOCATION, str(season))
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        self.logger.info(f"📊  Get Extracted data from :{latest_file_path}")
        return pd.read_csv(latest_file_path)

    def standardize_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize schema and split score column into home_score and away_score."""
        try:
            # Convert column names to lowercase
            df.columns = df.columns.str.lower()

            # Convert column "week" to int
            if "week" in df.columns:
                df["week"] = df["week"].astype("Int64")

            # Normalize datetime
            if "date" in df.columns and "time" in df.columns:
                df["time"] = df["time"].str.extract(r"\((\d{2}:\d{2})\)")
                df["time"] = df["time"].fillna("00:00")
                df["match_datetime"] = pd.to_datetime(
                    df["date"] + " " + df["time"],
                    format="%Y-%m-%d %H:%M",
                    errors="coerce",
                )
                df.drop(columns=["date", "time"], inplace=True, errors="ignore")

            # Normalize "home" and "away" columns (remove country prefix)
            if "home" in df.columns and "away" in df.columns:
                df["home"] = df["home"].str.replace(r"\s[a-z]{2,3}$", "", regex=True)
                df["away"] = df["away"].str.replace(r"^[a-z]{2,3}\s", "", regex=True)

            # Standardize "score" column (handle errors safely)
            if "score" in df.columns:
                df["score"] = df["score"].fillna("0-0").astype(str)

                # Remove text inside parentheses (e.g., "(4)")
                df["score"] = df["score"].apply(
                    lambda x: re.sub(r"\([^)]*\)", "", x).strip()
                )
                # Split into home and away scores
                df[["score_home", "score_away"]] = (
                    df["score"]
                    .str.split(
                        r"[–-]", expand=True
                    )  # Match both en dash (–) and hyphen (-)
                    .fillna("0")  # Ensure missing values are replaced
                    .astype("Int64")  # Convert to integer (nullable Int64)
                )
                df.drop(columns=["score"], inplace=True)
            # Convert "attendance" to int (handle missing values)
            if "attendance" in df.columns:
                df["attendance"] = (
                    df["attendance"]
                    .fillna("0")  # Replace NaN values with "0"
                    .astype(str)  # Convert to string for regex operations
                    .str.findall(
                        r"\d+"
                    )  # Find all digits in the string, returning a list
                    .str.join("")  # Join the list into a single string
                    .replace("", "0")  # Ensure empty strings are replaced with "0"
                    .astype("Int64")  # Convert to integer (nullable Int64)
                )

            return df

        except Exception as e:
            self.logger.error(f"❌ Standardization failed: {e}")
            raise  # Ensure proper error handling

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize dataset before loading into DB."""
        initial_rows = len(df)
        # 1. Rename columns to match database schema
        column_mapping = {"match report": "match_report"}
        df.rename(columns=column_mapping, inplace=True)

        # 2. Drop rows with missing values in important columns
        important_cols = [
            "season",
            "home",
            "away",
            "match_report",
        ]
        df = df.dropna(subset=important_cols)

        # 3. Convert data types
        df["season"] = pd.to_numeric(df["season"], errors="coerce").astype("Int64")
        df["week"] = pd.to_numeric(df["week"], errors="coerce").astype("Float64")

        # 4. Remove duplicate rows (keeping the first occurrence)
        df = df.drop_duplicates(subset=important_cols, keep="first")

        # 5. Ensure numeric values are valid
        df = df[(df["xg_home"] >= 0) & (df["xg_away"] >= 0)]

        # Log total rows removed
        final_rows = len(df)
        removed_rows = initial_rows - final_rows
        self.logger.info(f"✅ Total rows removed: {removed_rows} / {initial_rows}")

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
            self.LV2_SAVE_PATH, self.MATCHS_LOCATION, str(season)
        )
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        )
        df.to_csv(data_name, index=False)
        self.split_match_id(df, season)
        return df

    def split_match_id(self, df, season):
        """Split match id to a csv file"""
        now = datetime.datetime.now()
        folder_path = os.path.join(
            self.LV2_SAVE_PATH,
            self.MATCHS_LOCATION,
            str(season),
            self.MATCH_ID_DETAILS_LOCATION,
        )
        os.makedirs(folder_path, exist_ok=True)
        data_name = os.path.join(
            folder_path, f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        )
        df[["match_report"]].rename(columns={"match_report": "match_id"}).to_csv(
            data_name, index=False
        )
        return df


if __name__ == "__main__":
    transfomer = MatchTransformer()
    transfomer.transform_newest_data()

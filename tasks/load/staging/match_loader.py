from neon_loader import NeonLoader
import os


class MatchLoader(NeonLoader):
    def __init__(self):
        super().__init__()
        self.MATCHS_LOCATION = str(
            os.getenv("MATCHS_LOCATION")).upper()

    def load_data(self, season):
        """Main transform pipeline"""
        path = self.get_transformed_path(season)
        print(
            f"🔄 DEBUG : newest file in {path} \n load to table : {self.MATCHS_LOCATION} ")
        columns = ["season", "round", "week", "day", "home", "away", "xg_home", "xg_away",
                   "home_score", "away_score", "attendance", "venue", "referee", "match_report", "match_datetime"]

        self.load_csv(path, self.TABLE_SCORES_FIXTURES, columns=columns)
        print(
            f"✅  DEBUG : Load Done ")

    def get_transformed_path(self, season):
        """Load transformed data from file"""
        path = os.path.join(
            self.LV2_SAVE_PATH, self.MATCHS_LOCATION, str(season))
        if not os.path.exists(path):
            print(f"⚠️ WARNING: Directory {path} does not exist!")
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        return latest_file_path


if __name__ == "__main__":
    # ml = MatchLoader()
    # ld = ml.load_newest_data()

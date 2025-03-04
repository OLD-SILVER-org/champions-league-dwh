from tasks.load.staging.neon_loader import NeonLoader
import os


class SquadLoader(NeonLoader):
    def __init__(self):
        super().__init__()
        self.SQUADS_LOCATION = str(os.getenv("SQUADS_LOCATION")).upper()
        self.TABLE_SQUADS = os.getenv("TABLE_SQUADS")

    def load_data(self, season):
        """Main transform pipeline"""
        path = self.get_transformed_path(season)
        self.logger.info(
            f"📦 Newest file in {path} \n load to table : {self.SQUADS_LOCATION} "
        )
        columns = [
            "season",
            "nk",
            "country",
            "name",
            "number_of_player",
            "matches_played",
        ]
        self.load_csv(path, self.TABLE_SQUADS, columns=columns)

    def get_transformed_path(self, season):
        """Load transformed data from file"""
        path = os.path.join(self.LV2_SAVE_PATH, self.SQUADS_LOCATION, str(season))
        if not os.path.exists(path):
            self.logger.warning(f"⚠️ WARNING: Directory {path} does not exist!")
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        return latest_file_path


if __name__ == "__main__":
    ml = SquadLoader()
    ld = ml.load_newest_data()

from tasks.load.staging.neon_loader import NeonLoader
import os


class PlayerLoader(NeonLoader):
    def __init__(self):
        super().__init__()
        self.PLAYERS_LOCATION = str(os.getenv("PLAYERS_LOCATION")).upper()
        self.TABLE_PLAYERS = os.getenv("TABLE_PLAYERS")

    def load_data(self, season):
        """Main transform pipeline"""
        path = self.get_transformed_path(season)
        columns = [
            "season",
            "nk",
            "name",
            "nation",
            "positions",
            "squad_id",
            "squad",
            "born",
        ]

        self.load_csv(path, self.TABLE_PLAYERS, columns=columns)

    def get_transformed_path(self, season):
        """Load transformed data from file"""
        path = os.path.join(self.LV2_SAVE_PATH, self.PLAYERS_LOCATION, str(season))
        if not os.path.exists(path):
            self.logger.info("⚠️ WARNING: Directory %s does not exist!", path)
        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found
        latest_file = sorted(files, reverse=True)[0]
        latest_file_path = os.path.join(path, latest_file)
        # Read CSV and return DataFrame
        return latest_file_path


if __name__ == "__main__":
    ml = PlayerLoader()
    ld = ml.load_newest_data()

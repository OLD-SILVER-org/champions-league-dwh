from neon_loader import NeonLoader
import os


class MatchDetails(NeonLoader):
    def __init__(self, match_id=0):
        super().__init__()
        self.MATCH_DETAILS_LOCATION = str(
            os.getenv("MATCH_DETAILS_LOCATION")).upper()
        self.TABLE_MATCH_DETAILS = os.getenv("TABLE_MATCH_DETAILS")
        self.match_id = match_id

    def load_newest_data(self):
        self.load_data(self.match_id)
        pass

    def load_data(self, match_id):
        """Main transform pipeline"""
        path = self.get_transformed_path(match_id)
        print(
            f"🔄 DEBUG : newest file in {path} \n load to table : {self.MATCH_DETAILS_LOCATION} ")
        columns = [
            "match_id", "player_id", "shirt_number", "team_id",
            "goals", "own_goals", "yellow_cards", "red_card", "bench"
        ]

        self.load_csv(path, self.TABLE_MATCH_DETAILS, columns=columns)
        print(
            f"✅  DEBUG : Load Done ")

    def get_transformed_path(self, match_id):
        """Load transformed data from file"""
        path = os.path.join(
            self.LV2_SAVE_PATH, self.MATCH_DETAILS_LOCATION, str(match_id))
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
    ml = MatchDetails()
    ml.match_id = 19789895
    ld = ml.load_newest_data()

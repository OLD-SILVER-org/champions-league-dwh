import os
from tasks.load.staging.neon_loader import NeonLoader


class MatchDetailsLoader(NeonLoader):
    def __init__(self, match_id=0, season=2017):
        super().__init__()
        self.MATCH_DETAILS_LOCATION = str(os.getenv("MATCH_DETAILS_LOCATION")).upper()
        self.TABLE_MATCH_DETAILS = os.getenv("TABLE_MATCH_DETAILS")
        self.match_id = match_id
        self.season = season

    def load_newest_data(self):
        self.load_data(self.season)

    def load_data_by_season(self):
        self.load_data_by_season(self.season)

    def load_data_by_season(self, season):
        """Main transform pipeline. override abstract method. load data from load data from season"""
        match_ids = self.get_match_ids_by_season(season)
        if not match_ids:
            self.logger.warning(f"⚠️ No match data found for season {season}")
            return

        for match_id in match_ids:
            # set attribute
            self.match_id = match_id
            self.load_data()

    def load_data(self):
        """Main transform pipeline fro load data from self match_id and season"""
        path = self.get_transformed_path()
        if not path:
            self.logger.warning(
                f"⚠️ No transformed file found for match {self.match_id}"
            )
            return

        self.logger.info(
            f"🔄 Loading newest file in {path} \n to table: {self.MATCH_DETAILS_LOCATION}"
        )
        columns = [
            "match_id",
            "player_id",
            "shirt_number",
            "team_id",
            "goals",
            "own_goals",
            "yellow_cards",
            "red_card",
            "bench",
        ]

        self.load_csv(path, self.TABLE_MATCH_DETAILS, columns=columns)
        self.logger.info(f"✅ Load Done for match {match_id}")

    def get_transformed_path(self):
        """Load transformed data from file"""
        path = os.path.join(
            self.LV2_SAVE_PATH,
            self.MATCH_DETAILS_LOCATION,
            str(self.season),
            str(self.match_id),
        )
        if not os.path.exists(path):
            self.logger.warning(f"⚠️ WARNING: Directory {path} does not exist!")
            return None

        files = [f for f in os.listdir(path) if f.endswith(".csv")]
        if not files:
            return None  # No files found

        latest_file = sorted(files, reverse=True)[0]
        return os.path.join(path, latest_file)

    def get_match_ids_by_season(self, season):
        """Get match IDs by listing folders in the season directory"""
        season_path = os.path.join(
            self.LV2_SAVE_PATH, self.MATCH_DETAILS_LOCATION, str(season)
        )
        if not os.path.exists(season_path):
            self.logger.warning(
                f"⚠️ WARNING: Season directory {season_path} does not exist!"
            )
            return []

        match_ids = [
            folder
            for folder in os.listdir(season_path)
            if os.path.isdir(os.path.join(season_path, folder))
        ]
        return match_ids


if __name__ == "__main__":
    ml = MatchDetailsLoader()
    match_ids = ml.get_match_ids_by_season(2024)
    print(match_ids)

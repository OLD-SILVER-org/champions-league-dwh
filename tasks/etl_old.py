from tasks.etl_old_data.player_old_etl import PlayerOldETL
from tasks.etl_old_data.squad_old_etl import SquadOldETL
from tasks.etl_old_data.score_old_etl import ScoreOldETL
from tasks.etl_old_data.match_old_etl import MatchOldETL


class ETLOldData:
    def __init__(self):
        self.old_player_etl = PlayerOldETL()
        self.old_squad_etl = SquadOldETL()
        self.old_score_etl = ScoreOldETL()
        self.old_match_etl = MatchOldETL()
        pass

    def run(self):
        self.old_squad_etl.process()
        self.old_player_etl.process()
        self.old_score_etl.process()
        self.old_match_etl.process()
        pass


if __name__ == "__main__":
    etl = ETLOldData()
    etl.run()

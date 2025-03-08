from tasks.etl_player import ETL_player
from tasks.etl_squad import ETL_squad
from tasks.etl_score import ETL_score
from tasks.etl_match import ETL_match
from logs.logger import ETLLogger


class ETLMain:
    def __init__(self):
        self.etl_player = ETL_player()
        self.etl_squad = ETL_squad()
        self.etl_score = ETL_score()
        self.etl_match = ETL_match()
        self.logger = ETLLogger()
        pass

    def run(self):
        self.etl_player.run()
        self.logger.log("🚀 ✅ ETLPlayer Completed")
        self.etl_squad.run()
        self.logger.log("🚀 ✅ ETLSquad Completed")
        self.etl_score.run()
        self.logger.log("🚀 ✅ ETLScore Completed")
        self.etl_match.run()
        self.logger.log("🚀 ✅ ETLMatch Completed")
        pass


if __name__ == "__main__":
    etl_main = ETLMain()
    etl_main.run()

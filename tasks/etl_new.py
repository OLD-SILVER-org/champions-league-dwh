from tasks.etl_player import ETL_player
from tasks.etl_squad import ETL_squad
from tasks.etl_score import ETL_score
from tasks.etl_match import ETL_match


class ETLNew:
    def __init__(self):
        self.etl_player = ETL_player()
        self.etl_squad = ETL_squad()
        self.etl_score = ETL_score()
        self.etl_match = ETL_match()
        pass

    def run(self):
        self.etl_player.run()
        self.etl_squad.run()
        self.etl_score.run()
        self.etl_match.run()
        pass


if __name__ == "__main__":
    etl_main = ETLNew()
    etl_main.run()

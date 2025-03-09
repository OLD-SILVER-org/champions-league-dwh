from tasks.etl_new import ETLNew
from tasks.etl_old import ETLOldData
import os, sys


class ETLMain:
    def __init__(self):
        self.etl_new = ETLNew()
        self.etl_old = ETLOldData()

    def run_etl_old(self):
        print("Running ETL for old etl...")
        self.etl_old.run()

    def run_etl_new(self):
        print("Running ETL for NEW etl...")
        self.etl_new.run()


if __name__ == "__main__":
    etl = ETLMain()
    mode = sys.argv[1] if len(sys.argv) > 1 else "new"

    if mode == "old":
        etl.run_etl_old()
    elif mode == "new":
        etl.run_etl_new()
    else:
        print("Invalid ETL mode! Use 'old' or 'new'.")

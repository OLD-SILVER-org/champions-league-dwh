import logging
from logging.handlers import RotatingFileHandler
import os


class ETLLogger:
    _instance = None  # Singleton

    @staticmethod
    def get_logger():
        if ETLLogger._instance is None:
            ETLLogger._instance = logging.getLogger("ETL")
            ETLLogger._instance.setLevel(logging.INFO)

            # Make sure logs directory exists
            os.makedirs("logs", exist_ok=True)

            # Check if handler already exists to avoid duplicate logs
            if not ETLLogger._instance.handlers:
                # Create File Handler
                file_handler = RotatingFileHandler(
                    "logs/etl_process.log",
                    maxBytes=5 * 1024 * 1024,
                    backupCount=3,
                    encoding="utf-8",
                )
                file_handler.setFormatter(
                    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                )
                ETLLogger._instance.addHandler(file_handler)

                # Optional: Add StreamHandler to show logs on console
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(
                    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                )
                ETLLogger._instance.addHandler(console_handler)

        return ETLLogger._instance

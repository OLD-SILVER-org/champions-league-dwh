import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


class NeonStagingDB:
    """Manage connection to Neon PostgreSQL (Staging DB) using SQLAlchemy"""

    def __init__(self):
        self.db_url = os.getenv("NEON_URL")
        self.engine = None
        self.connect()

    def connect(self):
        """Establish connection"""
        if self.engine is None:
            try:
                self.engine = create_engine(self.db_url)
                print("✅ Connected to Neon PostgreSQL")
            except Exception as e:
                print(f"❌ Connection failed: {e}")

    def close(self):
        """Close database connection"""
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
            print("🔌 Connection closed.")

    def get_connection(self):
        """Get a raw database connection"""
        return self.engine.raw_connection()


# Example usage
if __name__ == "__main__":
    staging = NeonStagingDB()
    staging.close()

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class NeonStagingDB:
    """Manage connection to Neon PostgreSQL (Staging DB)"""

    def __init__(self):
        self.db_url = os.getenv("NEON_URL")
        self.conn = None

    def connect(self):
        """Establish connection"""
        if not self.conn:
            try:
                self.conn = psycopg2.connect(self.db_url)
                print("✅ Connected to Neon PostgreSQL")
            except Exception as e:
                print(f"❌ Connection failed: {e}")

    def execute_query(self, query, params=None, fetch=True):
        """Execute a SQL query"""
        if not self.conn:
            self.connect()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall() if fetch else None
        except Exception as e:
            print(f"❌ Query error: {e}")
            return None

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("🔌 Connection closed.")


if __name__ == "__main__":
    staging = NeonStagingDB()
    staging.connect()
    staging.close()
    pass

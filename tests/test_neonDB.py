import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
DATABASE_URL = os.getenv("NEON_URL")
print(f"✔ DATABASE_URL='{DATABASE_URL}'")  # Debug URL

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT '✅Connected to Neon PostgreSQL' AS status;"))
        print(result.fetchone()[0])
except Exception as e:
    print(f"❌ Connection fail: {e}")

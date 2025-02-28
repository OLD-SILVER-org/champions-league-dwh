CREATE TABLE scores_and_fixtures (
    id SERIAL PRIMARY KEY,
    season INT NOT NULL,
    round TEXT,
    week FLOAT,  -- Vì trong CSV `week` có thể chứa giá trị float (hoặc NULL)
    day TEXT,
    home TEXT NOT NULL,
    away TEXT NOT NULL,
    xg_home FLOAT,
    xg_away FLOAT,
    home_score INT,
    away_score INT,
    attendance INT,
    venue TEXT,
    referee TEXT,
    match_report TEXT,
    match_datetime TIMESTAMP
);

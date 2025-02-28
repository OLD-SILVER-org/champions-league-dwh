CREATE TABLE scores_and_fixtures (
    season INT,
    round TEXT,
    week FLOAT,
    day TEXT,
    home TEXT,
    xg_home FLOAT,
    xg_away FLOAT,
    away TEXT,
    attendance INT,
    venue TEXT,
    referee TEXT,
    match_report TEXT,
    match_datetime TIMESTAMP,
    home_score INT,
    away_score INT
);
CREATE TABLE squads (
    id SERIAL PRIMARY KEY,
    season INTEGER,
    nk TEXT,
    country TEXT,
    name TEXT,
    number_of_player INTEGER,
    matches_played INTEGER
);
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    season INTEGER,
    nk TEXT,
    name TEXT,
    nation TEXT,
    positions TEXT,
    squad_id TEXT,
    squad TEXT,
    born INTEGER
);
CREATE TABLE match_details (
    id SERIAL PRIMARY KEY,
    match_id INTEGER,
    player_id TEXT,
    shirt_number INTEGER,
    team_id TEXT,
    goals INTEGER,
    own_goals INTEGER,
    yellow_cards INTEGER,
    red_card INTEGER,
    bench BOOLEAN
);

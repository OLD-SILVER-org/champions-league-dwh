CREATE TABLE match_details (
    match_id TEXT,
    season TEXT,
    player_id TEXT,
    shirt_number INT,
    team_id TEXT,
    goals INT,
    own_goals INT,
    yellow_cards INT,
    red_card INT,
    bench BOOLEAN
);

CREATE TABLE players (
    player_id TEXT,
    season TEXT,
    name TEXT,
    nation TEXT,
    positions TEXT,
    squad_id TEXT,
    squad TEXT,
    born INT
);

CREATE TABLE scores_and_fixtures (
    id SERIAL,  -- ID tự tăng, không đặt PRIMARY KEY
    match_id TEXT,
    season TEXT,
    round TEXT,
    week INT,
    day TEXT,
    date DATE,
    home TEXT,
    xg_home FLOAT,
    score TEXT,
    xg_away FLOAT,
    away TEXT,
    attendance TEXT,
    venue TEXT,
    referee TEXT,
    match_report TEXT
);

CREATE TABLE squads (
    squad_id TEXT,
    season TEXT,
    country TEXT,
    name TEXT,
    num_players INT,
    matches_played INT
);

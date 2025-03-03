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
-- add column update_at
ALTER TABLE scores_and_fixtures ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
ALTER TABLE squads ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
ALTER TABLE match_details ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
ALTER TABLE players ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
-- create functions
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- create triggers
CREATE TRIGGER update_scores_and_fixtures
BEFORE UPDATE ON scores_and_fixtures
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER update_squads
BEFORE UPDATE ON squads
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER update_match_details
BEFORE UPDATE ON match_details
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER update_players
BEFORE UPDATE ON players
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

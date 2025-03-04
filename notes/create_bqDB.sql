CREATE TABLE `champions-league-dwh.fbref.dim_players` (
    id INT64,
    season INT64,
    player_nk STRING,
    name STRING,
    nation STRING,
    positions STRING,
    squad_nk STRING,
    squad_name STRING,
    born INT64,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE `champions-league-dwh.fbref.dim_squads` (
    id INT64,
    season INT64,
    squad_nk STRING,
    country STRING,
    squad_name STRING,
    number_of_player INT64,
    matches_played INT64,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE `champions-league-dwh.fbref.fact_scores` (
    id INT64,
    season INT64,
    round STRING,
    week INT64,
    day STRING,
    home_squad_nk STRING,
    xg_home_squad FLOAT64,
    xg_away_squad FLOAT64,
    away_squad_nk STRING,
    attendance INT64,
    venue STRING,
    referee STRING,
    match_nk STRING,
    home_score INT64,
    away_score INT64,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE `champions-league-dwh.fbref.fact_matches` (
    id INT64,
    match_nk STRING,
    player_nk STRING,
    shirt_number INT64,
    squad_nk STRING,
    goals INT64,
    own_goals INT64,
    yellow_cards INT64,
    red_card INT64,
    bench INT64,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

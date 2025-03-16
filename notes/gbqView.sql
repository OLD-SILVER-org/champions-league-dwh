CREATE OR REPLACE VIEW `champions-league-dwh.fbref.latest_fact_scores` AS
WITH latest_scores AS (
    SELECT * 
    FROM (
        SELECT *, 
               ROW_NUMBER() OVER (PARTITION BY match_nk ORDER BY updated_at DESC) AS rn
        FROM `champions-league-dwh.fbref.fact_scores`
    ) 
    WHERE rn = 1
)
SELECT * FROM latest_scores;

CREATE OR REPLACE VIEW `champions-league-dwh.fbref.latest_fact_matches` AS
WITH latest_matches AS (
    SELECT * 
    FROM (
        SELECT *, 
               ROW_NUMBER() OVER (PARTITION BY match_nk, player_nk ORDER BY updated_at DESC) AS rn
        FROM `champions-league-dwh.fbref.fact_matches`
    ) 
    WHERE rn = 1
)
SELECT * FROM latest_matches;


CREATE OR REPLACE VIEW `champions-league-dwh.fbref.latest_dim_players` AS
WITH latest_players AS (
    SELECT * 
    FROM (
        SELECT *, 
               ROW_NUMBER() OVER (PARTITION BY player_nk, squad_nk, season ORDER BY updated_at DESC) AS rn
        FROM `champions-league-dwh.fbref.dim_players`
    ) 
    WHERE rn = 1
)
SELECT * FROM latest_players;

CREATE OR REPLACE VIEW `champions-league-dwh.fbref.latest_dim_squads` AS
WITH latest_squads AS (
    SELECT * 
    FROM (
        SELECT *, 
               ROW_NUMBER() OVER (PARTITION BY squad_nk, season ORDER BY updated_at DESC) AS rn
        FROM `champions-league-dwh.fbref.dim_squads`
    ) 
    WHERE rn = 1
)
SELECT * FROM latest_squads;

CREATE OR REPLACE VIEW `champions-league-dwh.fbref.player_performance` AS
SELECT 
    fs.season,         
    fm.player_nk,
    dp.name,  
    SUM(fm.goals) AS total_goals,
    SUM(fm.yellow_cards) AS total_yellow_cards,
    SUM(fm.red_card) AS total_red_cards
FROM `champions-league-dwh.fbref.latest_fact_matches` fm
JOIN `champions-league-dwh.fbref.latest_fact_scores` fs  
    ON fm.match_nk = fs.match_nk  
JOIN `champions-league-dwh.fbref.latest_dim_players` dp
    ON fm.player_nk = dp.player_nk 
    AND fm.squad_nk = dp.squad_nk
    AND fs.season = dp.season  
GROUP BY fs.season, fm.player_nk, dp.name;


CREATE OR REPLACE VIEW `champions-league-dwh.fbref.squad_performance` AS
SELECT
    season,
    squad,
    SUM(wins) AS total_wins,
    SUM(losses) AS total_losses,
    SUM(draws) AS total_draws,
    (SUM(wins) + SUM(losses) + SUM(draws)) AS total_matches,
    ROUND(SUM(wins) * 100.0 / (SUM(wins) + SUM(losses) + SUM(draws)), 2) AS win_rate_percent,
    ROUND(SUM(losses) * 100.0 / (SUM(wins) + SUM(losses) + SUM(draws)), 2) AS loss_rate_percent,
    ROUND(SUM(draws) * 100.0 / (SUM(wins) + SUM(losses) + SUM(draws)), 2) AS draw_rate_percent
FROM (
    SELECT
        season,
        home_squad AS squad,
        COUNT(CASE WHEN home_score > away_score THEN 1 END) AS wins,
        COUNT(CASE WHEN home_score < away_score THEN 1 END) AS losses,
        COUNT(CASE WHEN home_score = away_score THEN 1 END) AS draws
    FROM `champions-league-dwh.fbref.fact_scores`
    GROUP BY season, home_squad

    UNION ALL

    SELECT
        season,
        away_squad AS squad,
        COUNT(CASE WHEN away_score > home_score THEN 1 END) AS wins,
        COUNT(CASE WHEN away_score < home_score THEN 1 END) AS losses,
        COUNT(CASE WHEN away_score = home_score THEN 1 END) AS draws
    FROM `champions-league-dwh.fbref.fact_scores`
    GROUP BY season, away_squad
)
GROUP BY season, squad
ORDER BY season DESC, win_rate_percent DESC;



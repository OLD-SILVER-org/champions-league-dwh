CREATE OR REPLACE VIEW `champions-league-dwh.fbref.player_performance` AS
SELECT 
    fs.season,         
    dp.name,         
    SUM(fm.goals) AS total_goals,
    SUM(fm.yellow_cards) AS total_yellow_cards,
    SUM(fm.red_card) AS total_red_cards
FROM `champions-league-dwh.fbref.fact_matches` fm
JOIN `champions-league-dwh.fbref.fact_scores` fs
    ON fm.match_nk = fs.match_nk  
JOIN `champions-league-dwh.fbref.dim_players` dp
    ON fm.player_nk = dp.player_nk 
    AND fm.squad_nk = dp.squad_nk
    AND fs.season = dp.season  
GROUP BY fs.season, dp.name;
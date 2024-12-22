CREATE TABLE game_info (
    game_date DATE NOT NULL,
    home_team VARCHAR(50) NOT NULL,
    away_team VARCHAR(50) NOT NULL,
    home_score INT NOT NULL,
    away_score INT NOT NULL,
    game_number INT NOT NULL,
    HP VARCHAR(50) NOT NULL,
    2B VARCHAR(50) NOT NULL,
    3B VARCHAR(50) NOT NULL,
    audience INT NOT NULL,
    time TIME NOT NULL,
    mvp_player VARCHAR(50),
    PRIMARY KEY (game_date, game_number) -- 定義複合主鍵
);

CREATE TABLE plate_appearances (
   game_date DATE NOT NULL,
   game_number INT NOT NULL,
   batter_id INT NOT NULL,
   pitcher_id INT NOT NULL,
   plate_appearance INT NOT NULL,
   PRIMARY KEY (game_date, game_number, batter_id, pitcher_id),
   FOREIGN KEY (game_date, game_number) REFERENCES game_info(game_date, game_number) ON DELETE CASCADE -- 如果 game_info 的 (game_data, game_number) 被刪掉 
   -- 則此表格對應的 （game_data, game_number) 也會被刪除
);

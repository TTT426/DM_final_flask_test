from app import db

class Player(db.Model):
    __tablename__ = 'players'
    player_name = db.Column(db.String(50), nullable=False)      # 姓名
    player_unique_id = db.Column(db.Integer, nullable=False, primary_key=True)  # 唯一的球員ID
    t_b = db.Column(db.String(50))                      # 投打習慣
    height = db.Column(db.Integer)                      # 身高
    weight = db.Column(db.Integer)                      # 體重
    born = db.Column(db.Date)                           # 生日
    debut = db.Column(db.Date)                          # 初登場
    nationality = db.Column(db.String(50))              # 國籍
    draft_order = db.Column(db.String(50))              # 選秀順位
    position = db.Column(db.String(50))                 # 位置

class Games(db.Model):
    __tablename__ = 'games'
    game_date = db.Column(db.Date, nullable=False)
    home_team = db.Column(db.String(50), nullable=False)
    away_team = db.Column(db.String(50), nullable=False)
    home_score = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer, nullable=False)
    game_number = db.Column(db.Integer, primary_key=True, nullable=False)
    HP = db.Column(db.String(50), nullable=True)
    first_base = db.Column(db.String(50), nullable=True, name="1B")  # 映射到數據庫中的 1B
    second_base = db.Column(db.String(50), nullable=True, name="2B") # 映射到數據庫中的 2B
    third_base = db.Column(db.String(50), nullable=True, name="3B")  # 映射到數據庫中的 3B
    audience = db.Column(db.Integer, nullable=True)
    game_time = db.Column(db.Integer, nullable=True)
    mvp_player = db.Column(db.String(50), nullable=True)
    game_status = db.Column(db.Integer, nullable=True)

class WinnerList(db.Model):
    __tablename__ = 'winner_list'
    years = db.Column(db.Integer, primary_key=True)                       # 年份
    most_hits_player_id = db.Column(db.Integer)                          # 安打王球員編號
    highest_batting_average_player_id = db.Column(db.Integer)            # 打擊王球員編號
    most_RBI_player_id = db.Column(db.Integer)                           # 打點王球員編號
    most_stolen_bases_player_id = db.Column(db.Integer)                  # 盜壘王球員編號
    homerun_leader_player_id = db.Column(db.Integer)                     # 全壘打王球員編號
    most_wins_player_id = db.Column(db.Integer)                          # 勝投王球員編號
    strikeout_leader_player_id = db.Column(db.Integer)                   # 奪三振王球員編號
    lowest_ERA_player_id = db.Column(db.Integer)                         # 防禦王球員編號
    most_saves_player_id = db.Column(db.Integer)                         # 最佳救援投手球員編號
    most_holds_player_id = db.Column(db.Integer)                         # 最佳中繼投手球員編號



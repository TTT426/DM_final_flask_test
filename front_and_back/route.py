from model import Player,Games,WinnerList,match_results,LeagueStats
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, text



def register_routes(app,db):
    #主頁連結
    @app.route('/')
    def home():
        return render_template('index.html')

    #一次顯示所有球員
    @app.route('/allPlayersWithoutTeam')
    def all_players():
        return render_template('allPlayersWithoutTeam.html')

    #球賽紀錄
    @app.route('/score')
    def score():
        return render_template('score.html')

    #歷年年度獎項讀主
    @app.route('/winnerlist')
    def winnerlist():
        return render_template('winnerList.html')

    #插入球員頁面
    @app.route('/insertplayer')
    def insertplayer():
        return render_template('insertPlayer.html')

    #插入比賽頁面
    @app.route('/insertgame')
    def insertgame():
        return render_template('insertGame.html')
    
    #球賽詳細資訊
    @app.route('/getgamedetail')
    def getgamedetail():
        return render_template('games_deatails.html')

    #個別球員詳細資料
    @app.route('/player')
    def player():
        return render_template('player.html')

    #預測功能
    @app.route('/predict')
    def predict():
        return render_template('predict.html')
    
    #更新球員資料庫
    @app.route('/updateplayer')
    def updateplayer():
        return render_template('updatePlayer.html')

    #更新年度獎項資料庫
    @app.route('/updatewinnerlist')
    def updatewinnerlist():
        return render_template('updateWinnerList.html')
    
    #刪除資料庫
    @app.route('/delete')
    def delete():
        return render_template('delete.html')

    #取得特定年分的年度獎項名單
    @app.route('/winnerlist/searchyear', methods=['GET'])
    def get_winner_list():
        # 從查詢參數中獲取年份
        year = request.args.get('years')
        
        # 檢查是否提供年份
        if not year:
            return jsonify({"error": "Year parameter is required"}), 400
        try:
            # 查詢年份的資料
            
            winner = WinnerList.query.filter_by(years=int(year)).first()
            # 檢查是否找到資料
            if not winner:
                print("error1\n")
                return jsonify({"error": f"No winners found for the year {year}"}), 404

            # 將查詢結果轉為字典格式返回
            result =[{
                "years": winner.years,
                "most_hits_player_id": winner.most_hits_player_id,
                "highest_batting_average_player_id": winner.highest_batting_average_player_id,
                "most_RBI_player_id": winner.most_RBI_player_id,
                "most_stolen_bases_player_id": winner.most_stolen_bases_player_id,
                "homerun_leader_player_id": winner.homerun_leader_player_id,
                "most_wins_player_id": winner.most_wins_player_id,
                "strikeout_leader_player_id": winner.strikeout_leader_player_id,
                "lowest_ERA_player_id": winner.lowest_ERA_player_id,
                "most_saves_player_id": winner.most_saves_player_id,
                "most_holds_player_id": winner.most_holds_player_id
            }]
            print(jsonify(result))
            return jsonify(result)

        except Exception as e:
            print("ok\n")
            return jsonify({"error": str(e)}), 500

    # API：取得球員詳細資料
    @app.route('/players/searchplayer', methods=['GET'])
    def get_player():
        # 從請求中獲取 player_unique_id 參數
        player_unique_id = request.args.get('player_unique_id')

        # 檢查是否提供 player_unique_id
        if not player_unique_id:
            return jsonify({"error": "Player unique ID is required"}), 400

        try:
            # 查詢資料庫中的球員資訊
            player = Player.query.filter_by(player_unique_id=int(player_unique_id)).first()

                # 如果未找到球員，返回錯誤訊息
            if not player:
                return jsonify({"message": "Player not found"}), 404

            # 將 ORM 對象轉換為字典格式返回
            result2 = [{
                    "player_name": player.player_name,
                    "player_unique_id": player.player_unique_id,
                    "number": player.number,
                    "t_b": player.t_b,
                    "height": player.height,
                    "weight": player.weight,
                    "born": player.born,
                    "debut": player.debut,
                    "nationality": player.nationality,
                    "draft_order": player.draft_order,
                    "position": player.position
            }]
            return jsonify(result2)

        except ValueError:
            return jsonify({"error": "Invalid player unique ID format"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    #回傳所有球員的id和名字
    @app.route('/player/getallplayer', methods=['GET'])
    def get_all_players():
        try:
            players = Player.query.all()
            if not players:
                return jsonify({"message": "No players found"}), 404

            # 將 ORM 對象轉換為 JSON
            result = [
                {
                    "player_name": player.player_name,
                    "player_unique_id": player.player_unique_id
                }
                for player in players
            ]
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    #用日期取得在該日期的所有球賽資訊
    @app.route('/games', methods=['GET'])
    def get_games_by_date():
        # 從請求中獲取 game_date 查詢參數
        game_date = request.args.get('game_date')

        # 驗證 game_date 是否存在
        if not game_date:
            return jsonify({"error": "game_date is required"}), 400

        try:
            print(game_date)
            # 查詢資料庫中符合 game_date 的比賽
            games = Games.query.filter_by(game_date=game_date).all()
            # 如果沒有找到比賽，返回提示訊息
            if not games:
                return jsonify({"message": f"No games found for the date {game_date}"}), 404

            # 將比賽數據轉為 JSON 格式返回
            results = []
            for game in games:
                results.append({
                    "game_date": game.game_date,
                    "home_team": game.home_team,
                    "away_team": game.away_team,
                    "home_score": game.home_score,
                    "away_score": game.away_score,
                    "game_number": game.game_number,
                    "hp": game.hp,
                    "first_base": game.first_base,
                    "second_base": game.second_base,
                    "third_base": game.third_base,
                    "audience": game.audience,
                    "game_time": game.game_time,
                    "game_status": game.game_status
                })

            return jsonify(results)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    #回傳最近三場的比賽資料
    @app.route('/latest-games', methods=['GET'])
    def get_latest_games():
        # 默認限制返回3場比賽
        limit = int(request.args.get('limit', 3))
        
        try:
            # 按日期降序排列並限制比賽數量
            games = Games.query.order_by(Games.game_date.desc()).limit(limit).all()

            if not games:
                return jsonify({"message": "No games found"}), 404

            # 將比賽數據轉為 JSON 格式返回
            results = []
            for game in games:
                results.append({
                    "game_date": game.game_date,
                    "home_team": game.home_team,
                    "away_team": game.away_team,
                    "home_score": game.home_score,
                    "away_score": game.away_score,
                    "game_number": game.game_number,
                    "hp": game.hp,
                    "first_base": game.first_base,
                    "second_base": game.second_base,
                    "third_base": game.third_base,
                    "audience": game.audience,
                    "game_time": game.game_time,
                    "game_status": game.game_status
                })

            return jsonify(results)

            

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    #刪除某一年的winnerlist
    @app.route('/winlist/delete', methods=['POST'])
    def delete_winlist_entry():
        data = request.get_json()
        year = data.get('year')

        # 檢查是否有提供年份
        if not year:
            return jsonify({"error": "Year is required"}), 400

        try:
            # 查詢資料庫中對應年份的資料
            winner = WinnerList.query.filter_by(years=year).first()

            if not winner:
                return jsonify({"message": f"No data found for year {year}"}), 404

            # 刪除資料
            db.session.delete(winner)
            db.session.commit()

            return jsonify({"message": f"Data for year {year} deleted successfully"}), 200

        except Exception as e:
            db.session.rollback()  # 回滾資料庫變更
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

    # 刪除比賽資料
    @app.route('/delete_game', methods=['POST'])
    def delete_game():
        data = request.get_json()
        game_date = data.get('game_date')
        game_number = data.get('game_number')

        # 驗證請求參數
        if not game_date or not game_number:
            return jsonify({"error": "Both 'game_date' and 'game_number' are required."}), 400

        try:
            # 確認日期格式
            game_date = datetime.strptime(game_date, "%Y-%m-%d").date()

            # 查詢資料庫中的比賽
            game = Games.query.filter_by(game_date=game_date, game_number=game_number).first()
            if not game:
                return jsonify({"error": "Game not found for the specified date and number."}), 404

            # 刪除比賽
            db.session.delete(game)
            db.session.commit()

            return jsonify({"message": "Game deleted successfully."}), 200

        except Exception as e:
            db.session.rollback()  # 發生異常時回滾變更
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    # 查詢投手對打者的比賽結果
    @app.route('/show-outcome', methods=['GET'])
    def show_outcome():
        pitcher_id = request.args.get('pitcher_id')
        batter_id = request.args.get('batter_id')
        year1 = request.args.get('year1')
        year2 = request.args.get('year2')

        # 檢查必要的參數是否存在
        if not pitcher_id or not batter_id or not year1 or not year2:
            return jsonify({'error': 'Missing required parameters'}), 400

        try:
            # 查詢符合條件的比賽結果
            battles = match_results.query.filter(
                match_results.pitcher_id == pitcher_id,
                match_results.batter_id == batter_id,
                match_results.year.between(year1, year2)
            ).all()

            # 構建回應資料
            if battles:
                battles_data = [
                    {
                        'year': battle.year,
                        'pitcher_id': battle.pitcher_id,
                        'batter_id': battle.batter_id,
                        'plate_appearances': battle.plate_appearances,
                        'at_bats': battle.at_bats,
                        'runs_batted_in': battle.runs_batted_in,
                        'hits': battle.hits,
                        'doubles': battle.doubles,
                        'triples': battle.triples,
                        'home_runs': battle.home_runs,
                        'total_bases': battle.total_bases,
                        'batting_average': battle.batting_average,
                        'walks': battle.walks,
                        'intentional_walks': battle.intentional_walks,
                        'hit_by_pitch': battle.hit_by_pitch,
                        'strikeouts': battle.strikeouts,
                        'on_base_percentage': battle.on_base_percentage
                    }
                    for battle in battles
                ]
                return jsonify({'success': True, 'battles': battles_data})

            return jsonify({'success': True, 'battles': []})

        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
    
    #計算給定投手和打者的ops+，若打者和投手無對戰紀錄。會特別通知前端
    @app.route('/calculate_ops_plus', methods=['GET'])
    def calculate_ops_plus():
        try:
            # 獲取請求中的參數
            player_id = request.args.get('player_id')  # 打者 ID
            pitcher_id = request.args.get('pitcher_id')  # 投手 ID
            start_year = int(request.args.get('start_year'))  # 開始年份
            end_year = int(request.args.get('end_year'))  # 結束年份

            # 查詢選定年份範圍內的打者和投手對戰紀錄
            player_stats = match_results.query.filter_by(player_unique_id=player_id).filter(
                match_results.year >= start_year, match_results.year <= end_year).all()
            
            pitcher_stats = match_results.query.filter_by(player_unique_id=pitcher_id).filter(
                match_results.year >= start_year, match_results.year <= end_year).all()

            # 判斷是否有對戰紀錄
            if not player_stats or not pitcher_stats:
                return jsonify({"error": "No game records found for the selected player and pitcher in the given years."}), 404

            # 計算打者的 OBP 和 SLG
            total_hits = sum(stat.hits for stat in player_stats)
            total_walks = sum(stat.bb for stat in player_stats)
            total_hbp = sum(stat.hbp for stat in player_stats)
            total_ab = sum(stat.ab for stat in player_stats)
            total_sf = sum(stat.sf for stat in player_stats)
            
            # 計算 OBP (On-base Percentage)
            obp = (total_hits + total_walks + total_hbp) / (total_ab + total_walks + total_hbp + total_sf)
            
            singles = sum(stat.singles for stat in player_stats)  # 單安打
            doubles = sum(stat.doubles for stat in player_stats)  # 二壘安打
            triples = sum(stat.triples for stat in player_stats)  # 三壘安打
            hr = sum(stat.hr for stat in player_stats)  # 全壘打
            
            # 計算 SLG (Slugging Percentage)
            slg = (singles + 2 * doubles + 3 * triples + 4 * hr) / total_ab

            # 查詢聯盟的平均 OBP 和 SLG
            league_obp = LeagueStats.query.filter(
                LeagueStats.year >= start_year, LeagueStats.year <= end_year).all()
            league_slg = LeagueStats.query.filter(
                LeagueStats.year >= start_year, LeagueStats.year <= end_year).all()
            
            if not league_obp or not league_slg:
                return jsonify({"error": "No league data found for the selected years."}), 404

            # 計算聯盟的平均 OBP 和 SLG
            league_obp_avg = sum(stat.obp for stat in league_obp) / len(league_obp)
            league_slg_avg = sum(stat.slg for stat in league_slg) / len(league_slg)

            # 計算 OPS+
            ops_plus = 100 * ((obp / league_obp_avg) + (slg / league_slg_avg) - 1)

            # 回傳結果
            result = {
                "player_id": player_id,
                "pitcher_id": pitcher_id,
                "start_year": start_year,
                "end_year": end_year,
                "OPS+": ops_plus
            }

            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    #新增新的資料進入player 
    @app.route('/add_player', methods=['POST'])
    def add_player():
        # 從前端接收 JSON 請求
        data = request.get_json()

        # 確保接收到必需的字段
        if not all(field in data for field in ['player_name','number', 't_b', 'height', 'weight', 'born', 'debut', 'nationality', 'draft_order', 'position']):
            return jsonify({"message": "Missing required fields"}), 400

        # 創建 Player 實例
        new_player = Player(
            player_name=data['player_name'],
            number=data['number'],
            t_b=data['t_b'],
            height=data['height'],
            weight=data['weight'],
            born=data['born'],
            debut=data['debut'],
            nationality=data['nationality'],
            draft_order=data['draft_order'],
            position=data['position']
        )

        # 儲存資料到資料庫
        try:
            db.session.add(new_player)
            db.session.commit()
            return jsonify({"message": "Player added successfully!", "player_unique_id": new_player.player_unique_id}), 201
        except Exception as e:
            db.session.rollback()  # 發生錯誤時回滾
            return jsonify({"message": f"Error: {str(e)}"}), 500
        
    @app.route('/insert_game', methods=['POST'])
    def insert_game():
        # 確保請求內容為 JSON 格式
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415

        try:
            # 獲取請求數據
            data = request.get_json()

            # 提取字段
            game_date = data.get('game_date')
            home_team = data.get('home_team')
            away_team = data.get('away_team')
            home_score = data.get('home_score')
            away_score = data.get('away_score')
            hp = data.get('hp')
            first_base = data.get('first_base')
            second_base = data.get('second_base')
            third_base = data.get('third_base')
            audience = data.get('audience')
            game_time = data.get('game_time')

            # 驗證必要字段是否存在
            if not game_date:
                return jsonify({"error": "Missing required fields"}), 400

            # 創建新遊戲記錄
            new_game = Games(
                game_date=game_date,
                home_team=home_team,
                away_team=away_team,
                home_score=home_score,
                away_score=away_score,
                hp=hp,
                first_base=first_base,
                second_base=second_base,
                third_base=third_base,
                audience=audience,
                game_time=game_time
            )

            # 保存到數據庫
            db.session.add(new_game)
            db.session.commit()

            return jsonify({"message": "Game inserted successfully"}), 201

        except Exception as e:
            db.session.rollback()  # 回滾數據庫
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
    @app.route('/game_details', methods=['GET'])
    def game_details():
        # 提取 URL 参数
        game_id = request.args.get('id')
        game_date = request.args.get('data')

        # 确保参数存在
        if not game_id or not game_date:
            return "Game ID and Date are required!", 400

        try:
            # 查詢資料庫中的比賽
            game = Games.query.filter_by(game_date=game_date, game_number=game_id).first()

            print(game)
            if not game:
                return jsonify({"error": "Game not found for the specified date and number."}), 404

            # 直接傳 html
            return render_template('game_details.html', game=game)

            

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # 查詢投手端點
    @app.route('/check-player', methods=['GET'])
    def check_player():
        player_name = request.args.get('name')  # 獲取前端傳遞的投手名字

        # 檢查是否提供了名字
        if not player_name:
            return jsonify({"error": "Player name is required"}), 400

        try:
            # 查詢符合名字的投手
            players = Player.query.filter(Player.player_name.like(f"%{player_name}%")).all()

            if not players:
                return jsonify({"exists": False, "players": []}), 200

            # 將查詢結果轉為字典
            player_list  =[]

            for player in players:
                 player_list.append({
                    "player_unique_id": player.player_unique_id,
                    "player_name": player.player_name,
                    "t_b": player.t_b,
                    "number":player.number,
                    "team":"樂天桃園",
                    "height": player.height,
                    "weight": player.weight,
                    "born": player.born,
                    "debut": player.debut,
                    "nationality": player.nationality,
                    "position": player.position,
                })

            return jsonify({"exists": True, "players": player_list}), 200

        except Exception as e:
             return jsonify({'exists': False, 'players': []}),500
        
    #更新player資訊
    @app.route('/players/<int:id>', methods=['PATCH'])
    def update_player(id):
        # 解析請求數據
        data = request.get_json()

        # 確保請求包含需要更新的數據
        required_fields = [
            "player_name", "number", "t_b", "height", "weight",
            "born", "debut", "nationality", "draft_order", "position"
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        try:
            # 根據 ID 查找球員
            player = Player.query.get(id)
            if not player:
                return jsonify({"error": "Player not found"}), 404

            # 更新球員信息
            player.player_name = data["player_name"]
            player.number = data["number"]
            player.t_b = data["t_b"]
            player.height = data["height"]
            player.weight = data["weight"]
            player.born = data["born"]
            player.debut = data["debut"]
            player.nationality = data["nationality"]
            player.draft_order = data["draft_order"]
            player.position = data["position"]

            # 保存更改到數據庫
            db.session.commit()

            return jsonify({"message": "Player updated successfully"}), 200

        except Exception as e:
            # 捕獲並處理異常
            db.session.rollback()
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
    # 更新得獎者列表資訊
    @app.route('/winnerlist/<int:year>', methods=['PATCH'])
    def update_winnerlist(year):

        data = request.get_json()
        # 根據年份查找相應的獲獎資料
        winner_data = WinnerList.query.filter_by(years=year).first()
        if not winner_data:
            return jsonify({"error": "Year not found"}), 404
        try:
            # 更新資料
            winner_data.most_hits_player_id = data.get('most_hits_player_id')
            winner_data.highest_batting_average_player_id = data.get('highest_batting_average_player_id')
            winner_data.most_RBI_player_id = data.get('most_RBI_player_id')
            winner_data.most_stolen_bases_player_id = data.get('most_stolen_bases_player_id')
            winner_data.homerun_leader_player_id = data.get('homerun_leader_player_id')
            winner_data.most_wins_player_id = data.get('most_wins_player_id')
            winner_data.strikeout_leader_player_id = data.get('strikeout_leader_player_id')
            winner_data.lowest_ERA_player_id = data.get('lowest_ERA_player_id')
            winner_data.most_saves_player_id = data.get('most_saves_player_id')
            winner_data.most_holds_player_id = data.get('most_holds_player_id')
            
            # 提交變更
            db.session.commit()
            return jsonify({"message": "Winner list updated successfully"}), 200

        except Exception as e:
            # 捕獲異常並回滾事務
            db.session.rollback()
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    # 搜尋球員
    @app.route('/search_player_bypartname', methods=['GET'])
    def search_players():
        player_name = request.args.get('player_name', '').strip()

        try:
            # 如果提供了 player_name，進行模糊搜尋
            if player_name:
                players = Player.query.filter(Player.player_name.ilike(f"%{player_name}%")).all()
            else:
                return jsonify({"error": "Missing 'player_name' parameter"}), 400

            # 將搜尋結果格式化為 JSON
                        # 將查詢結果轉為字典
            player_list  =[]
            a=34
            for player in players:
                 if(a<=34 and a>=0):
                    a=a-1
                    player_list.append({
                        "player_unique_id": player.player_unique_id,
                        "player_name": player.player_name,
                    })

            return jsonify(player_list), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500